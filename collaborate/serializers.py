from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import CurrentUserSerializer as BaseCurrentUserSerializer
from rest_framework import serializers


class UserSerializer(BaseUserSerializer):
    profile = serializers.ReadOnlyField(source='profile.id')

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('profile',)


class CurrentUserSerializer(BaseCurrentUserSerializer):
    profile = serializers.ReadOnlyField(source='profile.id')

    class Meta(BaseCurrentUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('profile',)
