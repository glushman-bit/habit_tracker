from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.validators import (
    DurationHabitValidator,
    PeriodicityValidator,
    PleasantHabitValidator,
    RelatedHabitIsPleasantValidator,
    RewardAndRelatedHabitValidator,
)
from users.models import User


class HabitsTestsCase(APITestCase):
    """TestsCase для привычек."""

    def setUp(self):
        self.user = User.objects.create(email='test@sky_pro')

        self.habit1 = Habit.objects.create(
            place='test_place',
            date_time='2026-07-07T20:00Z',
            action='test_action_pleasant',
            is_pleasant=True,
            related_habit=None,
            periodicity=1,
            reward=None,
            duration=60,
            is_public=True,
            owner=self.user,
        )
        self.habit2 = Habit.objects.create(
            place='test_place',
            date_time='2026-07-07T20:00Z',
            action='test_action_useful',
            is_pleasant=False,
            related_habit=self.habit1,
            periodicity=1,
            reward=None,
            duration=60,
            is_public=False,
            owner=self.user,
        )

    def test_create_habit(self):
        """Тест создания привычки."""

        url = reverse('habits:habit_create')
        data = {
            "place": "на работе",
            "date_time": "2026-07-07T17:41:00+03:00",
            "action": "помыть руки после работы",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": 60,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['action'], data['action'])
        self.assertEqual(response.json()['place'], data['place'])
        self.assertEqual(response.json()['duration'], data['duration'])
        self.assertEqual(response.json()['owner'], self.user.id)
        self.assertEqual(Habit.objects.count(), 3)

        latest_habit = Habit.objects.latest('id')
        self.assertEqual(latest_habit.action, "помыть руки после работы")
        self.assertEqual(latest_habit.owner, self.user)

    def test_update_habit(self):
        """Тест на редактирование привычки."""

        url = reverse('habits:habit_update', args=[self.habit1.id])
        data = {
            "place": "дома",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('place'), 'дома')

    def test_retrieve_habit(self):
        """Тест на просмотр привычки."""

        url = reverse('habits:habit_detail', args=[self.habit1.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'test_action_pleasant')

    def test_delete_habit(self):
        """Тест на удаление привычки владельцем и не владельцем."""

        url = reverse('habits:habit_delete', args=[self.habit1.id])
        self.user1 = User.objects.create(email='test_1@sky_pro')
        self.client.force_authenticate(user=self.user1)
        response_ = self.client.delete(url)

        self.assertEqual(response_.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.filter(pk=self.habit1.pk).count(), 0)

    def test_list_habits(self):
        """Тест на просмотр списка привычек."""

        url = reverse('habits:habit_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], Habit.objects.count())
        self.assertEqual(response.json()['next'], None)
        self.assertEqual(response.json()['previous'], None)

    def test_create_owner_habit(self):
        """Тест на автоматическое присвоение привычке владельца при создании."""

        url = reverse('habits:habit_create')
        self.client.force_authenticate(user=self.user)

        data = {
            "place": "на работе",
            "date_time": "2026-07-07T17:41:00+03:00",
            "action": "помыть руки после работы",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": 60,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)

        habit = Habit.objects.first()
        self.assertEqual(habit.owner, self.user)

    def test_full_sentence(self):
        """Тест на вывод полной информации о привычке, по полю 'full_sentence'."""

        url = reverse('habits:habit_list_public')
        self.client.force_authenticate(user=self.user)
        data = {
            "place": self.habit1.place,
            "date_time": self.habit1.date_time,
            "action": self.habit1.action,
            "is_public": True,
        }

        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'][0]['full_sentence'], "Я буду test_action_pleasant в 20:00 test_place"
        )


class ValidatorTestCase(TestCase):
    """TestCase для валидаторов."""

    def setUp(self):
        self.user1 = User.objects.create(email='test@sky_pro')
        self.habit4 = Habit.objects.create(
            place='test_place',
            date_time='2026-07-07T20:00Z',
            action='test_action_useful',
            is_pleasant=False,
            related_habit=None,
            periodicity=1,
            reward=None,
            duration=60,
            is_public=False,
            owner=self.user1,
        )
        self.validator = PleasantHabitValidator()
        self.validator1 = PeriodicityValidator(field='periodicity')
        self.validator2 = DurationHabitValidator(field='duration')
        self.validator3 = RelatedHabitIsPleasantValidator()
        self.validator4 = RewardAndRelatedHabitValidator()

    def test_is_pleasant_not_have_reward(self):
        """Тест, что у приятной привычки не может быть вознаграждения или связанной привычки."""

        data = {
            'is_pleasant': True,
            'reward': 'test_reward',
            'related_habit': None,
        }

        with self.assertRaises(ValidationError):
            self.validator(data)

    def test_periodicity_validator(self):
        """Тест запрета выполнять привычку реже 1 раза в неделю."""

        data = {
            'periodicity': 8,
        }

        with self.assertRaises(ValidationError):
            self.validator1(data)

    def test_duration_validator(self):
        """Тест времени выполнения привычки."""

        data = {
            'duration': 121,
        }

        with self.assertRaises(ValidationError):
            self.validator2(data)

    def test_relation_habit_validator(self):
        """Тест, что в связанные привычки можно добавлять только приятные привычки."""

        data = {'related_habit': self.habit4}

        with self.assertRaises(ValidationError):
            self.validator3(data)

    def test_relation_habit_reward_validator(self):
        """Тест, что у приятной привычки не может быть вознаграждения или связанной привычки."""

        data = {
            'reward': 'test_reward',
            'related_habit': self.habit4,
        }

        with self.assertRaises(ValidationError):
            self.validator4(data)
