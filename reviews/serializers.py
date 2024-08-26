from rest_framework import serializers


from books.api.serializers import BookSerializers
from reviews.models import Review
from users.serializers import UserSerializers


class ReviewSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    book = BookSerializers(read_only=True)

    def validate_rating(self, value):
        if 1 <= value <= 5:
            return value
        raise serializers.ValidationError("Рейтинг должен быть в диапазоне от 1 до 5.")


    class Meta:
        model = Review
        fields = '__all__'
