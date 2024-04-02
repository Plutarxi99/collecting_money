from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator

from config.settings import NULLABLE


class Collect(models.Model):
    class Status(models.IntegerChoices):
        BIRTHDAY = 0, 'День рожденья'
        WEDDING = 1, 'Свадьба'
        STARTUP = 2, 'Стартап'

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='author', **NULLABLE)
    title = models.CharField(max_length=120, verbose_name="Название сбора")
    reason = models.PositiveSmallIntegerField(verbose_name="Причина сбора")
    description = models.CharField(max_length=1_000, verbose_name="Описание сбора", **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name="Сумма сбора",
                                         validators=[
                                             MaxValueValidator(100_000_000,
                                                               message="Сумма не может превышать 100 млн руб")])
    amount_now = models.PositiveIntegerField(default=0, verbose_name="Сумма на данный момент")
    count_people = models.PositiveIntegerField(default=0, verbose_name="Количество людей сделавших пожертвований")
    photo = models.ImageField(upload_to="collect/", verbose_name="обложка сбора", **NULLABLE)
    end_of_event = models.DateTimeField(verbose_name="Конец сбора")
    donates = models.ManyToManyField("payment.Payment", related_name="donates", verbose_name="Донатеры", blank=True)

    class Meta:
        verbose_name = "Групповой сбор"
        verbose_name_plural = "Групповые сборы"
