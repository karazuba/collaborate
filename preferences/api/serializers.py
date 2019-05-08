from rest_framework import serializers

from preferences.models import CategoryPreference, ThemePreference, ProfilePreference
from publication.api.serializers.tag import CategorySerializer, ThemeSerializer
from account.api.serializers.profile import ProfileSerializer


class BasicPreferenceSerializer(serializers.Serializer):
    display = serializers.BooleanField()


class ThemePreferenceReadSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer()

    class Meta:
        model = ThemePreference
        fields = ('profile_id', 'theme', 'display')
        read_only_fields = fields


class CategoryPreferenceReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = CategoryPreference
        fields = ('profile_id', 'category', 'display')
        read_only_fields = fields


class ProfilePreferenceReadSerializer(serializers.ModelSerializer):
    subject_profile = ProfileSerializer

    class Meta:
        model = ProfilePreference
        fields = ('profile_id', 'subject_profile', 'display')
