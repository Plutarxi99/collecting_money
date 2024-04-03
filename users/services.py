from users.models import User


class MixinGetUser:
    def _user(self) -> dict:
        """
        Получение авторизированного пользователя, который делает запрос
        @return: словарь с почтой и иденфикатором его
        """
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            pk = User.objects.get(email=user).pk
            return {'user': user, 'pk': pk}
