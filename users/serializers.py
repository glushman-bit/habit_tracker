from django_countries.serializers import CountryFieldMixin
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(CountryFieldMixin, ModelSerializer):
    """Сериализатор для просмотра и изменения профиля"""

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "avatar", "country", "tg_nickname", "tg_chat_id")


class UserCreateSerializer(ModelSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):

        user = User(email=validated_data["email"], is_active=True)
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserViewSerializer(ModelSerializer):
    """Сериализатор представления данных о пользователях."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "avatar",
            "tg_nickname",
        )
