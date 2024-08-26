from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает доступ для суперпользователей для создания и удаления, а остальным пользователям только для чтения.
    """

    def has_permission(self, request, view):
        # Проверяем, является ли пользователь суперпользователем
        if request.user and request.user.is_superuser:
            return True

        # Разрешаем только безопасные методы для остальных пользователей
        return  request.user and (request.method in SAFE_METHODS)
