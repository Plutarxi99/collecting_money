from django.conf import settings
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from collect.models import Collect
from collect.schema import CollectSchema
from users.models import User
import random

from random import randrange
from datetime import timedelta


def random_date(days: int = 10):
    """
    Это функция для получения даты из будущего
    @param days: в какой промежуток дней получить рандомную дату по дефолту равно 10
    """
    start = now()
    end = start + timedelta(days=days)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


class Command(BaseCommand):
    """
    example: python3 manage.py addcol 10
    """
    help = 'Создает данные для группового сбора'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Указывает сколько пользователей необходимо создать')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        # получаем список всех id из таблицы users_user
        # list_id_user = User.objects.values_list("id", flat=True)
        list_id_user = User.objects.all()
        # список сумм, которые надо собрать
        list_amount = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
        for i in range(total):
            # берем рандомно один из id созданного user
            user = random.choice(list_id_user)
            # берем рандомную сумму
            amount = random.choice(list_amount)
            col = CollectSchema(
                author=user,
                title="Заголовок. Это тестовое наполнение базы данных",
                reason=random.choice(Collect.Reason.values),  # получение списка из возможных причин группового сбора
                description="Описание. Это тестовое наполнение базы данных",
                amount=amount,
                end_of_event=random_date(),
            )
            created, collect = Collect.objects.get_or_create(
                **col.model_dump()
            )

