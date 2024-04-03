from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Sum, Count

from config.settings import NULLABLE


class Collect(models.Model):
    class Reason(models.IntegerChoices):
        BIRTHDAY = 0, 'День рожденья'
        WEDDING = 1, 'Свадьба'
        STARTUP = 2, 'Стартап'

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='author', **NULLABLE)
    title = models.CharField(max_length=120, verbose_name="Название сбора")
    reason = models.PositiveSmallIntegerField(
        choices=Reason.choices,
        verbose_name="Причина сбора",
    )
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

    def save(
            self, *args, **kwargs
    ):
        if self.id:
            # получение списка кто задонатил групповому сбору
            col_list = self.donates.filter(status=True)
            # получение уникальных id донатеров и их подсчет
            col_list_donat_id = col_list.aggregate(count=Count("sender_id", distinct=True))["count"]
            # получение суммы донатов
            col_list_donat_amount = col_list.values_list("amount", flat=True).aggregate(total=Sum("amount"))["total"]
            self.count_people = col_list_donat_id if col_list_donat_id else 0
            self.amount_now = col_list_donat_amount if col_list_donat_amount else 0
        else:
            pass
        super(Collect, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Групповой сбор"
        verbose_name_plural = "Групповые сборы"
