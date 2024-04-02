from celery import shared_task
from collect.models import Collect
from payment.models import Payment
import time
import asyncio


async def status_pay():
    """
    Заглушка для обработки платеже и получение с сервера ответа об оплате
    @return:
    """
    answer_to_server = True
    return answer_to_server


@shared_task()
def add_and_save_amount_now(
        col: int,
        pay: int
):
    """
    Функция для добавления значение для M2M Collect.donates
    @param col: объект на который ссылается платеж
    @param pay: объект самого платежа
    """
    collect = Collect.objects.get(pk=col)
    payment = Payment.objects.get(pk=pay)
    status = asyncio.run(status_pay())
    if status:
        payment.status = status
        payment.save()
        payment.refresh_from_db()
        collect.amount_now += payment.amount
        collect.save()
        collect.refresh_from_db()
        return status
    else:
        payment.status = False
        payment.save()
        payment.refresh_from_db()
        return status
