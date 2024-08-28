from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserFactory
from users.models import User


class test_user(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

    def test_list_user(self):
        """
        Тест для проверки корректности возрврата всех пользователей
        :return:
        """
        UserFactory.create_batch(10)

        response = self.client.get(path='/api/users/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['results']), 5)

    def test_retrieve_user(self):
        """
        Тест для проверки корректности возвращения одного пользователя
        :return:
        """
        users = UserFactory.create_batch(10)

        user_to_retrieve = users[7]

        response = self.client.get(path=f'/api/users/{user_to_retrieve.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], user_to_retrieve.id)

    def test_create_user(self):
        """
        Тест для проверки создания пользователя
        :return:
        """
        user_data = {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "role": "user",
            "first_name": "John",
            "last_name": "Doe",
            "password": "your_secure_password",  # Обычно здесь будет хэш пароля
            "favorites": [],  # Это поле можно оставить пустым или добавить идентификаторы книг
        }
        response = self.client.post(path=f'/api/users/', data=user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.last()

        self.assertEqual(user.email, user_data['email'])  # так как это поле уникально

    def test_delete_user(self):
        """
        Тест для проверки удаления пользователя
        :return:
        """
        users = UserFactory.create_batch(10)
        user_to_delete = users[5]
        response = self.client.delete(path=f'/api/users/{user_to_delete.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        result = user_to_delete in User.objects.all()

        self.assertEqual(result, False)

    def test_update_user(self):
        """
        Тест для проверки обновления пользователя
        :return:
        """
        user = UserFactory.create()
        user_data = {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "role": "user",
            "first_name": "John",
            "last_name": "Doe",
            "password": "your_secure_password",  # Обычно здесь будет хэш пароля
            "favorites": [],  # Это поле можно оставить пустым или добавить идентификаторы книг
        }

        response = self.client.put(path=f'/api/users/{user.id}/', data=user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_structure_user(self):
        user_data = {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "role": "user",
            "first_name": "John",
            "last_name": "Doe",
        }

        # Создаем пользователя с помощью фабрики или напрямую
        user = UserFactory.create(**user_data)

        # Делаем GET-запрос для получения информации о пользователе
        response = self.client.get(path=f'/api/users/{user.id}/', format='json')

        # Проверяем, что статус-код ответа 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что структура данных совпадает с ожидаемой
        self.assertEqual(response.data['username'], user_data['username'])
        self.assertEqual(response.data['email'], user_data['email'])
        self.assertEqual(response.data['first_name'], user_data['first_name'])
        self.assertEqual(response.data['last_name'], user_data['last_name'])

    def test_user_cannot_delete_another_user(self):
        """
        Тест проверяет что пользователь не может удалить другого пользователя

        """

        user1 = UserFactory.create()
        user2 = UserFactory.create()


        self.client.force_authenticate(user=user1)


        response = self.client.delete(path=f'/api/users/{user2.id}/', format='json')


        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(User.objects.filter(id=user2.id).exists())
