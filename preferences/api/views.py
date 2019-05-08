from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.api.permissions import IsCurrentUserProfile
from account.api.views import ProfileUrlMixin
from preferences.api.serializers import (BasicPreferenceSerializer,
                                         CategoryPreferenceReadSerializer,
                                         ProfilePreferenceReadSerializer,
                                         ThemePreferenceReadSerializer)
from preferences.models import (CategoryPreference, ProfilePreference,
                                ThemePreference)
from tags.api.views import CategoryUrlMixin, ThemeUrlMixin


class BaseChangePreference(views.APIView):
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)

    def post(self, request, *args, **kwargs):
        serializer = BasicPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            new_display = serializer.data['display']
            preference, created = getattr(self, self.attr_name).preference_set \
                .get_or_create(profile=request.user.profile,
                               defaults={'display': new_display})
            if created or preference.display == new_display:
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            preference = getattr(self, self.attr_name).preference_set \
                .filter(profile=request.user.profile).get()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        preference.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeThemePreference(ThemeUrlMixin, BaseChangePreference):
    pass


class ChangeCategoryPreference(CategoryUrlMixin, BaseChangePreference):
    pass


class ChangeProfilePreference(ProfileUrlMixin, BaseChangePreference):
    pass


class ThemePreferenceList(ProfileUrlMixin, generics.ListAPIView):
    serializer_class = ThemePreferenceReadSerializer
    filterset_fields = ('display',)

    def get_queryset(self):
        return ThemePreference.objects.filter(profile=self.profile)


class CategoryPreferenceList(ProfileUrlMixin, generics.ListAPIView):
    serializer_class = CategoryPreferenceReadSerializer
    filterset_fields = ('display',)

    def get_queryset(self):
        return CategoryPreference.objects.filter(profile=self.profile)


class ProfilePreferenceList(ProfileUrlMixin, generics.ListAPIView):
    serializer_class = ProfilePreferenceReadSerializer
    filterset_fields = ('display',)

    def get_queryset(self):
        return ProfilePreference.objects.filter(profile=self.profile)
