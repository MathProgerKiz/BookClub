from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from books.api.serializers import BookSerializers
from books.permissions import IsAdminOrReadOnly
from reviews.send_email import send_new_book_notification
from users.models import User


@extend_schema(tags=['Book'])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'genre']
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'])
    def favorites(self, request, pk=None):
        """Метод для добавления книги в избранное пользователя"""
        book = self.get_object()
        user = request.user

        if user.favorites.filter(pk=book.pk).exists():
            return Response({'detail': 'Книга уже добавлена в избранное.'}, status=status.HTTP_400_BAD_REQUEST)

        user.favorites.add(book)
        return Response({'detail': 'Книга добавлена в избранное.'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """В данном методе пользователи будут получать уведомление о добавлении книги их любимых авторов,
           чьи книги находятся в избранном у пользователей.
        """
        # Создаем и валидируем сериализатор
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем объект книги
        self.perform_create(serializer)

        # Получаем сохраненный объект книги
        book = serializer.instance


        # Получаем автора книги
        author = book.author
        # Проходим по всем пользователям
        users = User.objects.all()
        for user in users:
            # Проверяем книги в избранном у пользователя
            for favorite in user.favorites.all():
                if favorite.author == author:
                    # Отправка уведомления
                    send_new_book_notification(user, book.title, book.get_absolute_url())
                    break  # Прекращаем цикл, если уведомление отправлено

        # Получаем заголовки для ответа
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
