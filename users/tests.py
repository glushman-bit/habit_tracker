from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersTestCase(APITestCase):
    """TestCase для пользователей."""

    def setUp(self):
        self.user1 = User.objects.create(email='user1@test.pro')
        self.user1.set_password('12345')
        self.user1.save()
        self.user2 = User.objects.create(email='user2@test.pro')
        self.user2.set_password('12345')
        self.user2.save()

    def test_create_user(self):
        """Тест создания пользователя."""

        url = reverse('users:register')
        data = {
            'email': 'user3@test.pro',
            'password': '12345',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

        user = User.objects.first()
        self.assertEqual(user.email, 'user1@test.pro')
        self.assertEqual(user.check_password('12345'), True)
        self.assertEqual(User.objects.count(), 3)

    def test_view_profile(self):
        """Тест на просмотр своего профиля."""

        url = reverse('users:users-detail', args=[self.user1.pk])
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tg_chat_id'], self.user1.tg_chat_id)

    def test_update_own_profile(self):
        """Тест редактирования своего профиля."""

        url = reverse('users:users-detail', args=[self.user1.pk])
        self.client.force_authenticate(user=self.user1)
        data = {'country': 'RU'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.country, 'RU')

    def test_view_other_profile(self):
        """Тест просмотр чужого профиля."""

        url = reverse('users:users-detail', args=(self.user2.pk,))
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user2.email)
        # Не можем посмотреть
        self.assertNotIn('phone_number', response.data)
        self.assertNotIn("country", response.data)
        # Можем посмотреть
        self.assertIn('avatar', response.data)
        self.assertIn('tg_nickname', response.data)

    def test_update_other_profile(self):
        """Тест редактирования чужого профиля."""

        url = reverse('users:users-detail', args=(self.user2.pk,))
        self.client.force_authenticate(user=self.user1)
        data = {'country': 'RU'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.user2.country, 'RU')
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.country, None)

    def test_view_list_users(self):
        """Просмотр списка пользователей."""

        url = reverse('users:users-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        data = response.data[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Не можем посмотреть
        self.assertNotIn('phone_number', data)
        self.assertNotIn("country", data)
        # Можем посмотреть
        self.assertIn('email', data)
        self.assertIn('tg_nickname', data)
