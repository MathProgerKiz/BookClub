import factory
from factory.django import DjangoModelFactory
from books.models import Book
from users.models import User  # Предполагается, что модель User находится в приложении users
from .models import Review

class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory('users.factories.UserFactory')  # Ссылка на фабрику User
    book = factory.SubFactory('books.factories.BookFactory')  # Ссылка на фабрику Book
    rating = factory.Faker('random_int', min=1, max=5)
    comment = factory.Faker('paragraph', nb_sentences=3)
    created_at = factory.Faker('date_time_this_year')

