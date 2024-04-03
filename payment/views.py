from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from collect.models import Collect
from payment.models import Payment
from payment.serializers import PaymentCreateSerializer, PaymentSerializer, MyPaymentListSerializers


class PaymentCreateAPIView(CreateAPIView):
    """
    Создание платежа
    """
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]


class MyPayListAPIView(ListAPIView):
    """
    Получение моих платежей
    """
    serializer_class = MyPaymentListSerializers
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(sender=user)

    @method_decorator(cache_page(timeout=60))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
