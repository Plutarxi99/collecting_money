from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from collect.models import Collect
from collect.task import send_mail_about_collect
from collect.validators import DatetimeValidator
from payment.models import Payment
from users.models import User


class CollectSerializer(ModelSerializer):
    class Meta:
        model = Collect
        fields = '__all__'


class CollectCreateSerializer(ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    amount_now = serializers.HiddenField(default=0)
    count_people = serializers.HiddenField(default=0)
    donates = serializers.HiddenField(default=[])

    def create(self, validated_data):
        """
        Дополнение при создании платежа, при платаже идет сохранения в объект Collect как платежа
        """
        collect: Collect = super().create(validated_data)
        # дополнение платежа в объект группового сбора
        # collect.donates.add(payment)
        send_mail_about_collect.delay(collect.pk)
        return validated_data

    class Meta:
        model = Collect
        fields = '__all__'
        validators = [
            DatetimeValidator(obj='self'),
        ]


class PaymentListForCollect(ModelSerializer):
    # для того, чтобы при получении ответа с по эндпоинту
    # в поле отправителя был почтовый адрес донатера
    sender = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = ("date_pay", "amount", "sender",)


class CollectAuthorSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='author', queryset=User.objects.all())

    class Meta:
        model = Collect
        fields = '__all__'


class CollectListSerializer(ModelSerializer):
    # для отображения донатов ввиде списка при получении ответа с эндпоинта
    donates = serializers.SerializerMethodField()
    # отображаем вместо id почту создателя
    author = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    def get_donates(self, instance: Collect):
        return PaymentListForCollect(instance.donates.filter(status=True), many=True).data

    class Meta:
        model = Collect
        fields = '__all__'


class CollectUpdateSerializer(ModelSerializer):
    class Meta:
        model = Collect
        fields = ('title', 'reason', 'description', 'end_of_event', 'photo', 'amount',)
        validators = [
            DatetimeValidator(obj='self'),
        ]
