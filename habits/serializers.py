from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    """Сериалайзер работы с привычками."""
    class Meta:
        model = Habit
        fields = '__all__'


class HabitPublicSerializer(ModelSerializer):
    """Сериалайзер вывода публичных привычек."""
    class Meta:
        model = Habit
        fields = ('id', 'action', 'place', 'time', 'duration', 'full_sentence')

