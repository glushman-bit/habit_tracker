from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitsListAPIView, HabitCreateAPIView, HabitDetailAPIView, HabitUpdateAPIView, \
    HabitDeleteAPIView, HabitPublicListAPIView


app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitsListAPIView.as_view(), name='habit_list'),
    path('public/', HabitPublicListAPIView.as_view(), name='habit_list_public'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('<int:pk>/', HabitDetailAPIView.as_view(), name='habit_detail'),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('<int:pk>/delete/', HabitDeleteAPIView.as_view(), name='habit_delete'),
]
