from payment.apps import PaymentConfig
from django.urls import path
from payment import views
app_name = PaymentConfig.name

urlpatterns = [
    path("create/", views.PaymentCreateAPIView.as_view(), name="payment_create"),
    path("my/", views.MyPayListAPIView.as_view(), name="payment_my"),
]
