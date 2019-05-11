from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.api.permissions import IsCurrentUserProfile
from accounts.api.views import ProfileUrlMixin
from recommendations.api.serializers import ThemeRecommendationSerializer
from recommendations.models import ThemeRecommendation


class ThemeRecommendationList(ProfileUrlMixin, generics.ListAPIView):
    url_kwarg = 'pk'
    serializer_class = ThemeRecommendationSerializer
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)

    def get_queryset(self):
        return ThemeRecommendation.objects.filter(profile=self.profile)
