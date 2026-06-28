from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils import timezone


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='Email пользователя',
        help_text='Укажите Email',
    )
    phone_number = PhoneNumberField(
        unique=True,
        blank=True,
        null=True,
        verbose_name='Phone Number',
        help_text='Укажите номер телефона'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        default='avatars/default.jpg',
        verbose_name='Загрузите аватар'
    )
    country = CountryField(
        blank_label="Country",
        help_text="Выберите страну",
        blank=True,
        null=True,
    )
    tg_nickname = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Ник в телеграмме",
        help_text="Укажите ник в ТГ"
    )
    tg_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Телеграмм chat-id",
        help_text="Укажите chat-id в телеграмм"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
