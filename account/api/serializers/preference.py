from rest_framework import serializers

from account.models import CategoryPreference, ThemePreference
from publication.api.serializers.tag import CategorySerializer, ThemeSerializer
from publication.models import Category, Theme


class ThemePreferenceReadSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer()

    class Meta:
        model = ThemePreference
        fields = ('profile', 'theme', 'display')
        read_only_fields = fields


class ThemePreferenceWriteSerializer(serializers.ModelSerializer):
    theme_id = serializers.PrimaryKeyRelatedField(
        queryset=Theme.objects.all())

    class Meta:
        model = ThemePreference
        fields = ('theme_id', 'display')


class CategoryPreferenceReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = CategoryPreference
        fields = ('profile', 'category', 'display')
        read_only_fields = fields


class CategoryPreferenceWriteSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = CategoryPreference
        fields = ('category_id', 'display')
