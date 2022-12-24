from djoser.serializers import UserCreateSerializer as BasicUserSerializer, UsernameResetConfirmSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(BasicUserSerializer):
    class Meta(BasicUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email','password', 'first_name', 'last_name']


class UserSerializer(BasicUserSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta(BasicUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email','password', 'first_name', 'last_name' ]


# class ResetUsernameConfirmSerializer(UsernameResetConfirmSerializer):
#     class Meta(BasicUserSerializer.Meta):
#         fields = ['uid', 'token', 'username' ]

