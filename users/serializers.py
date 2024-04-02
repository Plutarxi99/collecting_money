from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from payment.models import Payment
from payment.serializers import PaymentSerializer
from users.models import User
from users.services import MixinGetUser


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

    def get_user_pay(self, obj):
        return PaymentSerializer(Payment.objects.filter(sender=obj.id), many=True).data

    # def to_representation(self, instance):
    #     """Если пользователь обращается к своему профилю, то информация ограничивается"""
    #     ret = super().to_representation(instance)
    #     if self._user()['user'] == instance:
    #         return UserSerializer().data
    #     else:
    #         ret.pop('password')
    #         ret.pop('last_name')
    #         ret.pop('user_pay')
    #         return ret

    class Meta:
        model = User
        fields = '__all__'
