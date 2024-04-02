from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from collect.models import Collect
from collect.serializers import CollectSerializer
from payment.models import Payment
from payment.tasks import add_and_save_amount_now


# from payment.services.utils import add_and_save_amount_now


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
        collect.donates.add(payment)
        # TODO: добавить задачу в Celery
        number_task = add_and_save_amount_now.delay(col=collect.pk, pay=payment.pk)
        # result = number_task.status
        # if result == "SUCCESS":
        #     return validated_data
        # else:
        #     return validated_data
        return validated_data

    def to_representation(self, value):
        """
        Serialize the value's class name.
        """
        # value = {'sender': <User: admin@plut.arx>, 'amount': 1000, 'recipient': <Collect: Collect object (1)>}
        answer = {"message": f"Попoлнение на сумму {value['amount']} "
                             f"в групповой сбор {value['recipient'].title} "
                             f"Статус платежа смотри по users/my_pay"}
        return answer

    class Meta:
        model = Payment
        fields = '__all__'


