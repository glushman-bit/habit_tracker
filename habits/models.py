from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель привычки'
    )
    place = models.CharField(
        max_length=100,
        verbose_name='Место выполнения привычки'
    )
    time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Время выполнения привычки'
    )
    action = models.CharField(
        max_length=100,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name='Периодичность привычки (раз в день)',
    )
    reward = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Вознаграждение',
    )
    duration = models.IntegerField(
        verbose_name='Время выполнения привычки (в секундах)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f'{self.user}: в {self.time} выполняет {self.action} в {self.place}'
