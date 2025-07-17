"""Serializers for group project."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .constants import (EMAIL_PATTERN,
                        MAX_LENGTH_NAME,
                        MAX_USERNAME_LENGTH,
                        RESTRICTED_NAMES,
                        EMAIL_SUBJECT,
                        EMAIL_FROM
                        )
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_year
from .validators import validate_restricted_symbols


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    class Meta:
        """CategorySerializer."""

        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    """Genre serializer."""

    class Meta:
        """GenreSerializer metaclass."""

        model = Genre
        exclude = ['id']


class WriteTitleSerializer(serializers.ModelSerializer):
    """Serialazer to write Titles."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False
    )
    rating = serializers.IntegerField(default=None, read_only=True)
    year = serializers.IntegerField(
        default=None,
        validators=(validate_year,)
    )

    class Meta:
        """WriteTitle serializer meta class."""

        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        return ReadTitleSerializer(instance).data


class ReadTitleSerializer(serializers.ModelSerializer):
    """Serialazer to read Titles."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=None)

    class Meta:
        """ReadTitle serializer meta class."""

        model = Title
        fields = '__all__'
        read_only_fields = (fields,)


class BaseUserSerializer(serializers.ModelSerializer):
    """Base class for user serializer."""

    def validate_username(self, value):
        """Validate restricted names and symbols in username."""
        validate_restricted_symbols(value)
        if value in RESTRICTED_NAMES:
            raise serializers.ValidationError(
                f'Нельзя использовать имя {value}!')
        return value

    def validate_email(self, value):
        """Validate empty email."""
        if not EMAIL_PATTERN.fullmatch(value):
            raise serializers.ValidationError('Неправильный шаблон email!')
        return value


class UserSerializer(BaseUserSerializer):
    """User serializer."""

    username = serializers.CharField(max_length=MAX_USERNAME_LENGTH,
                                     required=True)
    email = serializers.CharField(max_length=MAX_LENGTH_NAME, required=True)

    class Meta:
        """Meta class for user serializer."""

        model = User
        fields = ('username', 'email',)

    def validate(self, attrs):
        """Validate for username and email."""
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=attrs['email'])
            except User.DoesNotExist:
                return attrs
        if attrs['username'] == user.username and attrs['email'] == user.email:
            return attrs
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                f"Пользователь {attrs['username']} уже есть в базе!"
            )
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                f"Электронная почта {attrs['email']} уже есть в базе!"
            )

    def create(self, validated_data):
        """Create new user."""
        user, _ = User.objects.get_or_create(
            username=validated_data.get('username'),
            defaults=validated_data
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=EMAIL_SUBJECT,
            message=confirmation_code,
            from_email=EMAIL_FROM,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return user


class JWTSerializer(serializers.Serializer):
    """JWT token serilaizer."""

    username = serializers.CharField(max_length=MAX_USERNAME_LENGTH)
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        """Validate symbols in username."""
        validate_restricted_symbols(value)
        return value

    def validate(self, attrs):
        """Validate confirmation code."""
        user = get_object_or_404(User, username=attrs['username'])
        if default_token_generator.check_token(user,
                                               attrs['confirmation_code']
                                               ):
            return attrs
        raise serializers.ValidationError('Не верный confirmation code!')


class ExtendedUserSerializer(BaseUserSerializer):
    """Serializer for another actions with user."""

    class Meta:
        """Meta class for serializer."""

        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',)


class ReviewSerializer(serializers.ModelSerializer):
    """Reviews Serializer."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True
                                          )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date', 'title']
        read_only_fields = ['title']

    def validate(self, data):
        """Check the uniqueness of the review."""
        request = self.context['request']

        if request.method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        if Review.objects.filter(author=request.user, title=title).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на это произведение."
            )

        data['title'] = title
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Comments Serializer."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True
                                          )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date', 'review']
        read_only_fields = ['review']


class UserMeSerializer(BaseUserSerializer):
    """User me serializer."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',)
        read_only_fields = ['role']
