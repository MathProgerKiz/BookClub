from rest_framework import status
from rest_framework.test import APITestCase

from books.factories import BookFactory
from books.models import Book
from users.factories import UserFactory


class TestBookCRUD(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

    def test_book_list_request(self):
        """
          Тест на проверку возращения всех книг пользователю

        """
        BookFactory.create_batch(10)
        url = "/api/books/"
        response = self.client.get(path=url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 10)
        self.assertEqual(len(response.data['results']), 5)

    def test_book_retrive(self):
        """
        Тест на проверку возвращения одной книги по id

        """
        book = BookFactory()
        BookFactory.create_batch(20)

        url = f'/api/books/{book.pk}/'
        responce = self.client.get(path=url, format='json')

        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        self.assertEqual(len(responce.data) // 6, 1)
        self.assertEqual(responce.data['id'], book.pk)

    def test_book_create(self):
        """
        Тест для проверки корректности создания книги
        """
        self.assertEqual(self.user.is_superuser, True)
        expected_id = Book.objects.all().count() + 1
        book_data = {
            "id": expected_id,
            "title": "Example Book Title",
            "author": "John Doe",
            "genre": "Fiction",
            "published_date": "2023-08-25 14:00:00",
            "average_rating": None,
            "description": "This is an example description of the book."
        }

        responce = self.client.post(path='/api/books/', data=book_data, format='json')

        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

        book = Book.objects.last()
        # self.assertEqual(book.pk, book_data['id'])
        self.assertEqual(book.title, book_data["title"])
        self.assertEqual(book.author, book_data["author"])
        self.assertEqual(book.genre, book_data["genre"])

        self.assertEqual(book.average_rating, book_data["average_rating"])
        self.assertEqual(book.description, book_data["description"])

    def test_book_delete(self):
        """
          Тест для проверки удаления книги
        """
        self.assertEqual(self.user.is_superuser, True)

        expected_id = Book.objects.all().count() + 1
        book_data1 = {
            "id": expected_id,
            "title": "Example Book Title",
            "author": "John Doe",
            "genre": "Fiction",
            "published_date": "2023-08-25 14:00:00",
            "average_rating": None,
            "description": "This is an example description of the book."
        }
        book_data = {

            "title": "Example Book Title",
            "author": "John Doe",
            "genre": "Fiction",
            "published_date": "2023-08-25 14:00:00",
            "average_rating": None,
            "description": "This is an example description of the book."
        }

        book_1 = Book.objects.create(**book_data)
        book_new = Book.objects.create(**book_data1)

        responce = self.client.delete(path=f'/api/books/{book_new.pk}/', format='json')

        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)

        book = Book.objects.last()
        self.assertNotEqual(book.pk, book_data1['id'])

    def test_put_book(self):
        """
          Тест для проверки корректности обновления записи
        """
        Book.objects.create(
            title="Sample Book",
            author="Sample Author",
            genre="Sample Genre",
            published_date="2023-01-01 10:00:00",
            average_rating=3,
            description="Sample Description"
        )

        book = Book.objects.first()
        if not book:
            self.fail("No book found in the database.")

        # Тестовые данные для обновления
        test_books_data = {
            'title': "Updated Title",
            'author': "Updated Author",
            'genre': "Updated Genre",
            'published_date': "2024-08-26 10:00:00",
            'average_rating': 4,
            'description': "Updated Description"
        }

        # Формируем URL для PUT-запроса
        url = f'/api/books/{book.pk}/'

        # Выполняем PUT-запрос для обновления записи
        response = self.client.put(path=url, data=test_books_data, format='json')

        # Проверяем, что статус ответа 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляем объект из базы данных
        book.refresh_from_db()

        # Проверяем, что все поля обновлены корректно
        self.assertEqual(book.title, test_books_data['title'])
        self.assertEqual(book.author, test_books_data['author'])
        self.assertEqual(book.genre, test_books_data['genre'])
        self.assertEqual(book.average_rating, test_books_data['average_rating'])
        self.assertEqual(book.description, test_books_data['description'])

    def test_add_book_to_favorites(self):
        test_books_data = {
            'title': "Updated Title",
            'author': "Updated Author",
            'genre': "Updated Genre",
            'published_date': "2024-08-26 10:00:00",
            'average_rating': 4,
            'description': "Updated Description"
        }
        book_favorite = Book.objects.create(**test_books_data)
        url = f'/api/books/{book_favorite.pk}/favorites/'
        responce = self.client.post(path=url, data=test_books_data, format='json')

        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        user_favorite_book = self.user.favorites.all()
        print(user_favorite_book)

        book_in_favorites = False
        for favorite_book in user_favorite_book:
            if book_favorite == favorite_book:
                book_in_favorites = True
                break

        self.assertEqual(book_in_favorites, True)

    def test_structure_list(self):
        test_books_data = {
            'title': "Updated Title",
            'author': "Updated Author",
            'genre': "Updated Genre",
            'published_date': "2024-08-26 10:00:00",
            'average_rating': 4,
            'description': "Updated Description"
        }

        book = Book.objects.create(**test_books_data)

        responce = self.client.get(path='/api/books/', format='json')

        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        test_book_data = {
            'id': responce.data['results'][0]['id'],
            'title': "Updated Title",
            'author': "Updated Author",
            'genre': "Updated Genre",
            'published_date': responce.data['results'][0]['published_date'],
            'average_rating': 4,
            'description': "Updated Description"
        }
        self.assertDictEqual(test_book_data, responce.data['results'][0])
