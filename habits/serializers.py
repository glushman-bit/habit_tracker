from rest_framework.serializers import ModelSerializer, SerializerMethodField

from habits.models import Habit

from .validators import (
    DurationHabitValidator,
    PeriodicityValidator,
    PleasantHabitValidator,
    RelatedHabitIsPleasantValidator,
    RewardAndRelatedHabitValidator,
)


class HabitSerializer(ModelSerializer):
    """Сериалайзер работы с привычками."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [
            PleasantHabitValidator(),
            PeriodicityValidator(
                field='periodicity',
            ),
            DurationHabitValidator(
                field='duration',
            ),
            RelatedHabitIsPleasantValidator(),
            RewardAndRelatedHabitValidator(),
        ]


class HabitPublicSerializer(ModelSerializer):
    """Сериалайзер вывода публичных привычек."""

    full_sentence = SerializerMethodField()

    class Meta:
        model = Habit
        fields = ('id', 'full_sentence', 'owner', 'is_public')
        read_only_fields = ('owner',)
        validators = []

    def get_full_sentence(self, obj):

        return f"Я буду {obj.action} в {obj.date_time.strftime('%H:%M')} в {obj.place}"
