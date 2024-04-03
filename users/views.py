from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from users.models import User
from users.serializers import UserSerializer, BaseUserSerializer, UserCreateSerializer


class UserPaymentListAPIView(RetrieveAPIView):
    """
    Получение списка платежей сделанным пользователем
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     user = self.request.user
    @method_decorator(cache_page(timeout=60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MyUserPaymentListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     user = self.request.user
    #     return queryset.filter(pk=user.pk)
    @method_decorator(cache_page(timeout=60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserCreateAPIView(CreateAPIView):
    """
    Для регистрации пользователя в приложении
    """
    serializer_class = UserCreateSerializer
