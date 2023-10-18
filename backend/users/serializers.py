import djoser.serializers
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser


class UserSerializer(djoser.serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email')
            )
        ]

    def get_is_subscribed(self, data):
        request = self.context.get('request')
        return request.user.is_authenticated and data.following.filter(
            username=request.user
        ).exists()


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password')
