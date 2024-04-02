from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from collect.models import Collect
from payment.models import Payment
from users.models import User


class CollectSerializer(ModelSerializer):
    class Meta:
        model = Collect
        fields = '__all__'


class CollectCreateSerializer(ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collect
        fields = '__all__'


class PaymentListForCollect(ModelSerializer):
    # для того, чтобы при получении ответа с по эндпоинту
    # в поле отправителя был почтовый адрес донатера
    sender = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = ("date_pay", "amount", "sender",)


class CollectListSerializer(ModelSerializer):
    # donates = PaymentListForCollect(source="recipient", read_only=True, many=True) # без добавления ORM команды
    # для отображения донатов ввиде списка при получении ответа с эндпоинта
    donates = serializers.SerializerMethodField()

    def get_donates(self, instance: Collect):
        return PaymentListForCollect(instance.donates, many=True).data

    class Meta:
        model = Collect
        fields = '__all__'
