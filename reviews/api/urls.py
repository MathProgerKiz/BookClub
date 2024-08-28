from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.api.views import ReviewsViewSet

router = DefaultRouter()
router.register(r'review', ReviewsViewSet)
urlpatterns = [
    path('', include(router.urls))
]
