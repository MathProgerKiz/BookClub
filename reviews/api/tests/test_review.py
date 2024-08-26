from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from books.factories import BookFactory
from books.models import Book
from reviews.factories import ReviewFactory
from reviews.models import Review
from users.factories import UserFactory


class test_api_review(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

    def test_list_review_book(self):
        """
        Тест на проверку возвращения всех отзывов определенной книги

        """
        book_data = {
            "title": "Example Book Title",
            "author": "John Doe",
            "genre": "Fiction",
            "published_date": "2023-08-25 14:00:00",
            "average_rating": None,
            "description": "This is an example description of the book."
        }

        # Создаем книгу
        book = Book.objects.create(**book_data)

        # Создаем 20 отзывов для этой книги
        ReviewFactory.create_batch(7, book=book)

        # Формируем URL для запроса отзывов конкретной книги
        url = f'/api/review/?book={book.pk}'

        # Выполняем GET-запрос для получения отзывов
        response = self.client.get(path=url, format='json')

        # Проверяем, что статус ответа 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе содержится 20 отзывов

        self.assertEqual(len(response.data['results']), 5)  # с учетом пагинации

    def test_list_review_user(self):
        """
         Тест на проверку возвращения всех отзывов определенного юзера
        """

        ReviewFactory.create_batch(3, user=self.user)

        url = f'/api/review/?user={self.user.id}'

        response = self.client.get(path=url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['results']), 3)

    def test_create_review(self):
        """
          Тест для проверки создания отзыва

        """

        book = BookFactory.create()

        url = f'/api/review/'
        review_data = {
            'user': self.user.id,
            'book': book.id,
            'rating': 4,
            'comment': "This book is very good",
        }

        response = self.client.post(path=url, data=review_data, format='json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("Ошибка 400: ", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        review = Review.objects.last()

        self.assertIsNotNone(review, "Объект не создался ")

        self.assertEqual(review.user.pk, self.user.id)
        self.assertEqual(review.book.pk, book.pk)
        self.assertEqual(review.rating, 4)

    def test_review_delete(self):
        """
         Тест для проверки корректности удаления
        :return:
        """
        book = BookFactory.create()
        review = ReviewFactory.create(user=self.user, book=book)

        ReviewFactory.create_batch(5)

        url = f'/api/review/{review.id}/'

        response = self.client.delete(path=url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Review.objects.count(), 5)

        self.assertEqual(book.reviews.filter(id=review.id).count(), 0)
        self.assertEqual(self.user.reviews.count(), 0)
