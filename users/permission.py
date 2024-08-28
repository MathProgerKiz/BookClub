from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает доступ для суперпользователей для создания и удаления, а остальным пользователям только для чтения.
    """


    def has_object_permission(self, request, view, obj):
        # Проверяем, что метод безопасный (например, GET, HEAD, OPTIONS) - разрешаем доступ
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Проверяем, что текущий пользователь является владельцем объекта
        return obj == request.user or request.user.is_superuser