from rest_framework import serializers
from books.models import Book
from reviews.models import Review
from users.models import User


class ReviewSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Обработка через идентификатор
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # Обработка через идентификатор

    def validate_rating(self, value):
        if 1 <= value <= 5:
            return value
        raise serializers.ValidationError("Рейтинг должен быть в диапазоне от 1 до 5.")

    class Meta:
        model = Review
        fields = ['user', 'book', 'rating', 'comment', 'created_at']  # Явное перечисление полей
