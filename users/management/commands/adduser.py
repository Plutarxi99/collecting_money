from django.conf import settings
from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from users.models import User


class Command(BaseCommand):
    """
    example: python3 manage.py adduser 10 -P test -M gmail
    """
    help = 'Создает случайных пользователей'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int,
                            help='Указывает сколько пользователей необходимо создать')

        # Опциональный аргумент
        parser.add_argument('-P', '--prefix', type=str,
                            help='Префикс имени пользователя', )

        # Флаг
        parser.add_argument('-A', '--admin', action='store_true',
                            help='Дать пользователю права администратора')

        # Опциональный аргумент
        parser.add_argument('-M', '--mail', type=str,
                            help='Дать пользователю имя почтового сервиса')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        prefix = kwargs['prefix']
        admin = kwargs['admin']
        mail = kwargs['mail']

        for i in range(total):
            if prefix and mail:
                email = f'{prefix}{get_random_string(2)}@{mail}.ru'
            elif prefix:
                email = f'{prefix}{get_random_string(2)}@bk.ru'
            elif mail:
                email = f'{get_random_string(7)}@{mail}.ru'
            else:
                email = f'{get_random_string(7)}@bk.ru'

            if admin:
                user, created = User.objects.get_or_create(
                    email=settings.SUPERUSER_EMAIL,
                    is_staff=True,
                    is_superuser=True,
                    is_active=True,
                )
                if created or not user.check_password(raw_password=settings.SUPERUSER_PASSWORD):
                    user.set_password(raw_password=settings.SUPERUSER_PASSWORD)
                    user.save()
            else:
                user, created = User.objects.get_or_create(
                    email=email,
                    is_active=True,
                )
                if created or not user.check_password(raw_password=settings.USER_PASSWORD):
                    user.set_password(raw_password=settings.USER_PASSWORD)
                    user.save()
