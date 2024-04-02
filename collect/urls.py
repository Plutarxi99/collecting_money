from collect.apps import CollectConfig
from django.urls import path
from collect import views
app_name = CollectConfig.name

urlpatterns = [
    path("create/", views.CollectCreateAPIView.as_view(), name="collect_create"),
    path("all/", views.CollectListAPIView.as_view(), name="collect_all_list"),
    path("my/", views.CollectMyListAPIView.as_view(), name="collect_my_list"),
    path("update/<int:pk>/", views.CollectUpdateAPIView.as_view(), name="collect_update"),
    path("delete/<int:pk>/", views.CollectDestroyAPIView.as_view(), name="collect_destroy"),
]
