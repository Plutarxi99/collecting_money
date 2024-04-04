from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer


class UserPaymentListAPIView(RetrieveAPIView):
    """
    Получение списка платежей сделанным пользователем
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(timeout=60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# class MyUserPaymentListAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     @method_decorator(cache_page(timeout=60))
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    """
    Для регистрации пользователя в приложении
    """
    serializer_class = UserCreateSerializer
