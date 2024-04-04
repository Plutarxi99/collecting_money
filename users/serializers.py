from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from collect.models import Collect
from payment.models import Payment
from users.models import User
from users.services import MixinGetUser


class PaymentSerializerForUser(ModelSerializer):
    recipient = SlugRelatedField(slug_field='title', queryset=Collect.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(MixinGetUser, ModelSerializer):
    user_pay = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Удалите все поля, которые не указаны в аргументе `fields`.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_user_pay(self, instance):
        list_pay = Payment.objects.filter(sender=instance)
        return PaymentSerializerForUser(list_pay, many=True).data

    def to_representation(self, instance):
        """Если пользователь обращается к своему профилю, то информация ограничивается"""
        ret = super().to_representation(instance)
        if self._user()['user'] == instance.email:
            return BaseUserSerializer()
        else:
            # ret.pop('password')
            # ret.pop('last_login')
            # ret.pop('is_superuser')
            # ret.pop('is_staff')
            # ret.pop('is_active')
            # ret.pop('date_joined')
            # ret.pop('groups')
            # ret.pop('user_permissions')
            return ret

    class Meta:
        model = User
        fields = ('id', 'email', 'last_name', 'user_pay',)
