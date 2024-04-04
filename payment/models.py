from django.contrib.auth import get_user_model
from django.db import models

from collect.models import Collect
from config.settings import NULLABLE


class Payment(models.Model):
    date_pay = models.DateTimeField(auto_now_add=True, verbose_name="Время платежа")
    amount = models.PositiveIntegerField(default=1, verbose_name="Сумма платежа")
    recipient = models.ForeignKey(Collect, on_delete=models.SET_NULL,
                                  **NULLABLE, related_name="recipient",
                                  verbose_name="Получатель")
    sender = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               **NULLABLE, related_name="sender",
                               verbose_name="Отправитель")
    status = models.BooleanField(default=False, verbose_name="Статус платежа")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
