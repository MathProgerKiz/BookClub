from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from reviews.models import Review
from reviews.rating import rating_update
from reviews.serializers import ReviewSerializers


@extend_schema(tags=['Reviews'])
class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'rating', 'user']

    def create(self, request, *args, **kwargs):
        """При добавлении отзыва на книгу ее средняя оценка меняется"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_data = request.data.get('book')

        if isinstance(book_data, dict):
            book_pk = book_data.get('id')
        else:
            return Response({'error': 'Invalid book data'}, status=status.HTTP_400_BAD_REQUEST)

        if not book_pk:
            return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(pk=book_pk)
        except:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_create(serializer)

        new_rating = request.data.get('rating')
        if new_rating is not None:
            rating_update(book, new_rating)
        else:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
