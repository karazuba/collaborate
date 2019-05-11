from rest_framework import serializers

from recommendations.models import ThemeRecommendation
from tags.api.serializers import ThemeSerializer

class ThemeRecommendationSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer()

    class Meta:
        model = ThemeRecommendation
        fields = ('profile_id', 'theme', 'estimated_rating')