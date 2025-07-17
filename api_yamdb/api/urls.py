"""api urls."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CreateUserViewSet,
    CommentViewSet,
    GenreViewSet,
    get_jwt_token,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet
)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('auth/signup', CreateUserViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('api/v1/auth/token/', get_jwt_token),
    path('api/v1/', include(router_v1.urls)),
]
