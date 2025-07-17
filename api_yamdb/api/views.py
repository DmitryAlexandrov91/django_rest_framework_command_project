"""Views function and CBVs for group project."""

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .mixins import GenreCategoryViewSet
from .permissions import AdminOrReadOnly, IsAdmin, ReviewsCommentsPermissions
from .serializers import (CategorySerializer, CommentSerializer,
                          ExtendedUserSerializer, GenreSerializer,
                          JWTSerializer, ReadTitleSerializer, ReviewSerializer,
                          UserMeSerializer, UserSerializer,
                          WriteTitleSerializer)

User = get_user_model()


class CategoryViewSet(GenreCategoryViewSet):
    """CategoryViewSet."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryViewSet):
    """GenreViewSet."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """TitleViewSet."""

    queryset = (Title.objects.annotate
                (rating=Avg('reviews__score')).order_by('year'))
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        """Choise serializers for self.action."""
        if self.action in ['list', 'retrieve']:
            return ReadTitleSerializer
        return WriteTitleSerializer


@api_view(['POST'])
def get_jwt_token(request):
    """Get jwt_token Api function."""
    serializer = JWTSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User,
                             username=serializer.data.get('username'))
    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token), },
                    status=status.HTTP_200_OK)


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Create user view set."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Creation new user."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Another actions (without CREATE) with user's model."""

    queryset = User.objects.all()
    serializer_class = ExtendedUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated],
            serializer_class=UserMeSerializer)
    def me(self, request):
        self.kwargs['username'] = request.user.username
        return self.retrieve(request)

    @me.mapping.patch
    def patch_me(self, request, *args, **kwargs):
        self.kwargs['username'] = request.user.username
        return self.partial_update(request)


class ReviewViewSet(viewsets.ModelViewSet):
    """Review Viewset."""

    serializer_class = ReviewSerializer
    permission_classes = (ReviewsCommentsPermissions,)
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Comments ViewSet."""

    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ReviewsCommentsPermissions,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Getting the review and title objects based on URL parameters."""
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        review = self.get_review()
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        """Creating the comment for the specific review."""
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
