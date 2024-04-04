from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from collect.models import Collect
from payment.models import Payment
from payment.tasks import add_and_save_amount_now


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        """
        Дополнение при создании платежа, при платаже идет сохранения в объект Collect как платежа
        """
        collect: Collect = validated_data["recipient"]
        payment: Payment = super().create(validated_data)
        # дополнение платежа в объект группового сбора
        # collect.donates.add(payment)
        add_and_save_amount_now.delay(col=collect.pk, pay=payment.pk)
        return validated_data

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        answer = {"message": f"Попoлнение на сумму {value['amount']} "
                             f"в групповой сбор {value['recipient'].title} "
                             f"Статус платежа смотри по users/my_pay"}
        return answer

    class Meta:
        model = Payment
        fields = '__all__'


class MyPaymentListSerializers(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
