from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

from collect.models import Collect


@shared_task()
def send_mail_about_collect(collect_pk):
    """
    Задача отлоеженная на отправку сообщений с созданием группового сбора
    @param collect_pk:
    @return:
    """
    collect = Collect.objects.get(pk=collect_pk)
    try:
        send_mail(
            subject="Вы создали групповой сбор",
            message=f"Группой сбор имеет название: {collect.title}"
                    f"Сумму, которую хотите набрать: {collect.amount}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[collect.author]
        )
        return {'status': True, 'response': "Сервер отработал как надо"}
    except BaseException as error:
        return {'status': False, 'response': error}
