from celery import shared_task
from django.conf import settings

from collect.models import Collect
from payment.models import Payment
import asyncio
from django.core.mail import send_mail


async def status_pay():
    """
    Заглушка для обработки платеже и получение с сервера ответа об оплате
    @return:
    """
    answer_to_server = True
    return answer_to_server


def send_mail_about_pay(status, payment):
    try:
        send_mail(
            subject="Состояние вашего платежа",
            message=f"Платежный сервер прислал такой ответ {status}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[payment.sender]
        )
        return {'status': True, 'response': "Сервер отработал как надо"}
    except BaseException as error:
        return {'status': False, 'response': error}


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
        collect.donates.add(payment)
        collect.save()
        collect.refresh_from_db()

    else:
        payment.status = False
        payment.save()
        payment.refresh_from_db()
    result = send_mail_about_pay(status, payment)
    return result
