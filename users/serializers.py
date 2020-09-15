from rest_framework import serializers

from users.models import User


class UserActivitySerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("last_login", "last_action")


class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
