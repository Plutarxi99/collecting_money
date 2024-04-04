from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated)

from collect.models import Collect
from collect.permissions import IsUserCreator
from collect.serializers import (CollectCreateSerializer,
                                 CollectListSerializer,
                                 CollectUpdateSerializer)

from rest_framework import parsers
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class CollectCreateAPIView(CreateAPIView):
    """
    Создание группового сбора. Выбор reason
    BIRTHDAY = 0, 'День рожденья'
    WEDDING = 1, 'Свадьба'
    STARTUP = 2, 'Стартап'

    Создание объекта группового сбора:

        title: Название вашего группового сбора
        ---
        reason: Причина группового сбора
        ---
        description: Описание вашего группового сбора
        ---
        amount: Сумма на которую вы рассчитываете
        ---
        photo: Фотография вашего сбора
        ---
        end_of_event: Конец вашего сбора

    """
    serializer_class = CollectCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)

    @swagger_auto_schema(request_body=CollectCreateSerializer)
    def create(self, request, *args, **kwargs):
        new_obj = super(CollectCreateAPIView, self).create(request, *args, **kwargs)
        return new_obj


class CollectListAPIView(ListAPIView):
    """
    Получение всех групповых сборов
    """
    serializer_class = CollectListSerializer
    queryset = Collect.objects.all().order_by('id')
    permission_classes = [AllowAny]

    @method_decorator(cache_page(timeout=60))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CollectMyListAPIView(ListAPIView):
    """
    Получение моих групповых сборов
    """
    serializer_class = CollectListSerializer
    queryset = Collect.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(author=user)

    @method_decorator(cache_page(timeout=60))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CollectUpdateAPIView(UpdateAPIView):
    """
    Обновление группового сбора
    """
    queryset = Collect.objects.all()
    serializer_class = CollectUpdateSerializer
    permission_classes = [IsAuthenticated, IsUserCreator]


class CollectDestroyAPIView(DestroyAPIView):
    """
    Удаление группового сбора
    """
    queryset = Collect.objects.all()
    permission_classes = [IsAuthenticated, IsUserCreator]
