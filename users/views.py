from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializers


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
