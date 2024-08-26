from rest_framework import serializers

from books.models import Book


class BookSerializers(serializers.ModelSerializer):

    def validate_average_rating(self, value):
        if value is not None:
            if 1 <= value <= 5:
                return value
            raise serializers.ValidationError("Рейтинг должен быть в диапазоне от 1 до 5.")
        return value

    class Meta:
        model = Book
        fields = "__all__"
