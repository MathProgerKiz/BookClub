import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password
from .models import User

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = factory.Faker('random_element', elements=['admin', 'user'])
    password = factory.LazyFunction(lambda: make_password('defaultpassword'))

    @factory.post_generation
    def favorites(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Если передан список книг, добавляем их к избранным пользователям
            for book in extracted:
                self.favorites.add(book)
