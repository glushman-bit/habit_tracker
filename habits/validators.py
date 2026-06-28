from dataclasses import field

from rest_framework.exceptions import ValidationError


class PleasantHabitValidator:
    """Проверка, что у приятной привычки не может быть вознаграждения или связанной привычки."""
    def __call__(self, attrs):
        is_pleasant = attrs.get('is_pleasant')
        reward = attrs.get('reward')
        related_habit = attrs.get('related_habit')

        if is_pleasant and (reward or related_habit):
            raise ValidationError("У приятной привычки не может быть собственного вознаграждения или связанной привычки.")


class PeriodicityValidator:
    """Нельзя выполнять привычку реже 1 раза в неделю."""

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        periodicity = attrs.get(self.field)

        if periodicity and periodicity > 7:
            raise ValidationError(
                {self.field: "Нельзя выполнять привычку реже 1 раза в 7 дней."}
            )


class DurationHabitValidator:
    """Проверка времени выполнения привычки."""
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        duration = attrs.get(self.field)

        if duration and duration > 120:
            raise ValidationError(
                {self.field: "Время выполнения не может быть больше 120 секунд."}
            )


class RelatedHabitIsPleasantValidator:
    """Проверка, что в связанные привычки можно добавлять только приятные привычки."""

    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                {"related_habit": "В связанные привычки можно добавлять привычки с признаком приятной."}
            )


class RewardAndRelatedHabitValidator:
    """Проверка, что у приятной привычки не может быть вознаграждения или связанной привычки."""

    def __call__(self, attrs):
        reward = attrs.get('reward')
        related_habit = attrs.get('related_habit')

        if reward and related_habit:
            raise ValidationError(
                "Нельзя выбрать вознаграждение и связанную привычку."
            )
