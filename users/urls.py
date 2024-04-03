from users import views
from users.apps import UsersConfig
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pay/<int:pk>/', views.UserPaymentListAPIView.as_view(), name='other_user_payment'),
    path('pay/my/', views.MyUserPaymentListAPIView.as_view(), name='my_payment'),
    path('register/', UserCreateAPIView.as_view(), name='register_user'),
]
