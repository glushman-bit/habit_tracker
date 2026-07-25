from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .permissions import IsProfile
from .serializers import UserCreateSerializer, UserSerializer, UserViewSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователями."""

    queryset = User.objects.all()
    # serializer_class = UserViewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Права доступа для изменения профиля пользователя."""

        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsProfile]

        return super().get_permissions()

    def get_serializer_class(self):
        """Переопределение сериалайзера для просмотра профиля пользователя.
        Добавлена защита от ошибки построения схемы Swagger."""

        if getattr(self, 'swagger_fake_view', False):
            return UserSerializer

        if self.action == 'retrieve':
            user = self.get_object()

            if user != self.request.user:
                return UserViewSerializer

        elif self.action == 'list':
            return UserViewSerializer

        return UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Класс создания пользователя."""

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
