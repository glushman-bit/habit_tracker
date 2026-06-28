from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, UserCreateSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    """Класс создания пользователя."""

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
