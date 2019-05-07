from rest_framework import serializers

from account.models import CategoryPreference, ThemePreference, ProfilePreference
from publication.api.serializers.tag import CategorySerializer, ThemeSerializer
from account.api.serializers.profile import ProfileSerializer


class BasicPreferenceSerializer(serializers.Serializer):
    display = serializers.BooleanField()


class ThemePreferenceReadSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer()

    class Meta:
        model = ThemePreference
        fields = ('profile', 'theme', 'display')
        read_only_fields = fields


class CategoryPreferenceReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = CategoryPreference
        fields = ('profile', 'category', 'display')
        read_only_fields = fields


class ProfilePreferenceReadSerializer(serializers.ModelSerializer):
    subject_profile = ProfileSerializer

    class Meta:
        model = ProfilePreference
        fields = ('profile', 'subject_profile', 'display')
