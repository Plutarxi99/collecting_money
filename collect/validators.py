from rest_framework.exceptions import ValidationError
from django.utils.timezone import now


class DatetimeValidator:
    """
    Валидатор для проверки поля end_of_event,
    что его значение было в будущем
    """

    def __init__(self, obj):
        self.obj = obj

    def __call__(self, obj):
        datetime_now = now()
        end_of_event = dict(obj).get("end_of_event")
        if datetime_now >= end_of_event:
            raise ValidationError("Конец группового сбора должен завершиться в будущем")
