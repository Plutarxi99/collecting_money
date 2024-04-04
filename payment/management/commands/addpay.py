from django.core.management import BaseCommand

from collect.models import Collect
from payment.models import Payment
from payment.schema import PaymentSchema

from users.models import User
import random


class Command(BaseCommand):
    """
    example: python3 manage.py addpay 10
    """
    help = 'Создает данные для платежей и присваение их групповым сборам'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int,
                            help='Указывает сколько пользователей необходимо создать')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        # получаем список из таблицы User
        # list_id_user = User.objects.values_list("id", flat=True)
        list_id_user = User.objects.all()
        # получаем список из таблицы Collect
        list_collect = Collect.objects.all()
        # список сумм, которые надо собрать
        dict_amount = {"a": 1, "b": 10_000_000}
        for i in range(total):
            # рандомно берем сумму пополнений
            amount = random.randint(a=dict_amount["a"], b=dict_amount["b"])
            # берем рандомно один из id созданного user
            user = random.choice(list_id_user)
            # берем рандомно получателя пожертвований
            recipient: Collect = random.choice(list_collect)
            pay = PaymentSchema(
                amount=amount,
                recipient=recipient,
                sender=user,
                status=random.choice((True, False))
            )
            payment = Payment.objects.create(
                **pay.model_dump()
            )
            recipient.donates.add(payment)
            recipient.save()
