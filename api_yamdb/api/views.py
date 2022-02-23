from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.custom_viewsets import (ListCreateDestroyViewSet,
                                 RetrieveListCreateDestroyPartialUpdateViewSet)
from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsModerator, IsOwner, IsSuperuser,
                             ReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTokenSerializer, MeSerializer,
                             RegistrationsSerializer, ReviewSerializer,
                             TitleCreateSerializer, TitleSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def registrations(request):
    serializer = RegistrationsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, _ = User.objects.get_or_create(email=email, username=username)
    token = default_token_generator.make_token(user)
    send_mail(
        'Ваш confirmation_code',
        f'Для пользователя {username} выпущен '
        f'confirmation_code: {token}',
        settings.EMAIL_SENDER,
        [f'{email}'],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.data['username']
    )
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(
        user,
        confirmation_code
    ):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet модели кастомного пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin | IsSuperuser]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def me_endpoint(self, request):
        user = request.user
        user = get_object_or_404(User, username=user.username)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ReviewViewSet(RetrieveListCreateDestroyPartialUpdateViewSet):
    """
    ViewSet модели Review. Позволяет работать с постами.
    Имеет функции: CRUD
    """
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        (ReadOnly | IsAdmin | IsModerator | IsOwner)
    ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        # Добавил условие, чтобы в консоли не отображалась ошибка при
        # генерации документации yasg
        if getattr(self, 'swagger_fake_view', False):
            return Title.objects.none()
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()


class CommentViewSet(RetrieveListCreateDestroyPartialUpdateViewSet):
    """
    ViewSet модели Comment. Позволяет работать с комментариями пользователей.
    Имеет функции: CRUD
    """
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        (ReadOnly | IsAdmin | IsModerator | IsOwner)
    ]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, title_id=self.kwargs['title_id'],
                                   id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        # Добавил условие, чтобы в консоли не отображалась ошибка при
        # генерации документации yasg
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        review = get_object_or_404(
            Review, title_id=self.kwargs['title_id'],
            id=self.kwargs['review_id'],
        )
        return review.comments.all()


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    ViewSet предназначен для просмотра списка категорий (типы)
    произведений, создания и удаления категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [IsAdmin | IsSuperuser | ReadOnly]


class GenreViewSet(ListCreateDestroyViewSet):
    """
    ViewSet предназначен для просмотра списка категорий жанров, создания и
    удаления жанра
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = [IsAdmin | IsSuperuser | ReadOnly]
    lookup_field = 'slug'


class TitleViewSet(RetrieveListCreateDestroyPartialUpdateViewSet):
    """
    ViewSet предоставляет CRUD действия с произведения, к которым пишут
    отзывы (определённый фильм, книга или песенка).
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAdmin | IsSuperuser | ReadOnly]

    def get_serializer_class(self):
        # в зависимости от действия выбираем тот или иной сериалайзер
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleSerializer
