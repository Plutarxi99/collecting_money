from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from collect.models import Collect
from collect.serializers import CollectSerializer
from payment.models import Payment
from payment.serializers import PaymentSerializer
from users.models import User
from users.services import MixinGetUser


class PaymentSerializerForUser(ModelSerializer):
    recipient = SlugRelatedField(slug_field='title', queryset=Collect.objects.all())

    class Meta:
        model = Payment
        exclude = ('sender',)


class UserSerializer(MixinGetUser, ModelSerializer):
    user_pay = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        # Не передавайте аргумент 'fields' в суперкласс
        fields = kwargs.pop('fields', None)

        # Создайте экземпляр суперкласса обычным образом
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

    class Meta:
        model = User
        fields = '__all__'
