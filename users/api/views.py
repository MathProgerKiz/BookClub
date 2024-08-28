from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from users.models import User
from users.api.serializers import UserSerializers
from users.permission import IsAdminOrReadOnly


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAdminOrReadOnly]
