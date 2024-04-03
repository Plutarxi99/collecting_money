from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from config.settings import NULLABLE
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Создание суперпользователя, если уже пользователь существует,
        то ошибки не будет
        """
        user = self.get(
            email=email
        )
        if not user:
            user = self.create_user(
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def has_one_of_groups(self, *groups: str) -> bool:
        groups_filter = Q()
        for group_name in groups:
            groups_filter |= Q(name=group_name)
        return self.groups.filter(groups_filter).exists()

    # def __str__(self):
    #     return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
