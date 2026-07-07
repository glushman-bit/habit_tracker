from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsProfile
from .serializers import UserSerializer, UserCreateSerializer, UserViewSerializer
from .models import User


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
        """Переопределение сериалайзера для просмотра профиля пользователя."""

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
