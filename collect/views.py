from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from collect.models import Collect
from collect.serializers import (CollectSerializer,
                                 CollectCreateSerializer,
                                 CollectListSerializer)


class CollectCreateAPIView(CreateAPIView):
    """
    Создание группового сбора
    """
    serializer_class = CollectCreateSerializer
    queryset = Collect.objects.all()
    permission_classes = [IsAuthenticated]


class CollectListAPIView(ListAPIView):
    """
    Получение всех групповых сборов
    """
    serializer_class = CollectListSerializer
    queryset = Collect.objects.all()
    permission_classes = [IsAuthenticated]


class CollectMyListAPIView(ListAPIView):
    """
    Получение моих групповых сборов
    """
    serializer_class = CollectSerializer
    queryset = Collect.objects.all()
    permission_classes = [IsAuthenticated]


class CollectUpdateAPIView(UpdateAPIView):
    """
    Обновление группового сбора
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticated]


class CollectDestroyAPIView(DestroyAPIView):
    """
    Удаление группового сбора
    """
    queryset = Collect.objects.all()
    permission_classes = [IsAuthenticated]