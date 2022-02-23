import re

from django.db.models import Avg
from rest_framework import validators
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        SerializerMethodField, ValidationError)

from reviews.models import Category, Comment, Genre, Review, Title, User


class RegistrationsSerializer(ModelSerializer):
    """Сериализатор для регистрацции нового пользователя"""
    username = CharField(
        max_length=150,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = EmailField(
        max_length=254,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError(
                'Имя пользователя не может быть me')
        if not re.match(r'^[\w.@+-]', data['username']):
            raise ValidationError(
                'Имя пользователя может содержать буквы, цифры, '
                'символы ".", "@", "+", "-", " "'
            )
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class GetTokenSerializer(ModelSerializer):
    """Сериализатор получения авторизационного токена"""
    username = CharField()
    confirmation_code = SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)

    def get_confirmation_code(self, obj):
        return


class UserSerializer(ModelSerializer):
    """Сериализатор для модели кастомного пользователя"""
    email = EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role',)


class MeSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role',)

    def update(self, instance, validated_data):
        user = get_object_or_404(User, username=instance)
        print(user)
        if user.role == 'user' and 'role' in validated_data:
            validated_data.pop('role')
        return super().update(instance, validated_data)


class ReviewSerializer(ModelSerializer):
    """Сериализатор модели Review."""
    author = SlugRelatedField(slug_field='username', read_only=True)
    text = CharField(allow_blank=True, required=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review

    def validate(self, data):
        """Проверка на лимит в 1 отзыв на 1 произведение."""
        author = self.context['request'].user
        title = self.context['view'].kwargs['title_id']
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=author, title=title).exists()
        ):
            raise ValidationError(
                'Вы уже оставляли отзыв к данному произведению!'
            )
        return data


class CommentSerializer(ModelSerializer):
    """Сериализатор модели Comment."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment


class CategorySerializer(ModelSerializer):
    """Сериализатор категорий произведений"""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(ModelSerializer):
    """Сериализатор жанра произведения"""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(ModelSerializer):
    """Сериализатор списка произведений"""
    rating = SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class TitleCreateSerializer(ModelSerializer):
    """Сериализатор для создания/обновления произведения"""
    genre = SlugRelatedField(queryset=Genre.objects.all(),
                             slug_field='slug', many=True)
    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
