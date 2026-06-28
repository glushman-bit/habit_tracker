from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitsListAPIView(ListAPIView):
    """Класс вывода списка привычек."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = []
    # pagination_class = Pass


class HabitCreateAPIView(CreateAPIView):
    """Класс создания привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = []

    def perform_create(self, serializer):
        """Автоматически определяем владельца при создании."""

        serializer.save(user=self.request.user)


class HabitDetailAPIView(RetrieveAPIView):
    """Класс просмотра информации о привычке."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = []


class HabitUpdateAPIView(UpdateAPIView):
    """Класс редактирования привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = []


class HabitDeleteAPIView(DestroyAPIView):
    """Класс удаления привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = []
