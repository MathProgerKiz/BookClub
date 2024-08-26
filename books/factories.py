import factory
from factory.django import DjangoModelFactory
from .models import Book  # Импортируем вашу модель Book


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author = factory.Faker('name')
    genre = factory.Faker('word')
    published_date = factory.Faker('date_time_this_decade')
    average_rating = factory.Faker('random_int', min=1, max=5)
    description = factory.Faker('paragraph', nb_sentences=3)

