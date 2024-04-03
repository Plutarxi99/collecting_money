from rest_framework.permissions import BasePermission


class IsUserCreator(BasePermission):
    """
    Класс для запрета модерирование не своих групповых сборов
    """

    def has_permission(self, request, view):
        if view.get_object().author == request.user:
            return True
        return False
