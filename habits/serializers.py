from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from .validators import PleasantHabitValidator, PeriodicityValidator, DurationHabitValidator, RelatedHabitIsPleasantValidator, RewardAndRelatedHabitValidator


class HabitSerializer(ModelSerializer):
    """Сериалайзер работы с привычками."""
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [
            PleasantHabitValidator(),
            PeriodicityValidator(field='periodicity',),
            DurationHabitValidator(field='duration',),
            RelatedHabitIsPleasantValidator(),
            RewardAndRelatedHabitValidator(),
        ]


class HabitPublicSerializer(ModelSerializer):
    """Сериалайзер вывода публичных привычек."""
    class Meta:
        model = Habit
        fields = ('id', 'action', 'place', 'time', 'duration', 'full_sentence')

