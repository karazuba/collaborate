from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, views
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from account.api.permissions import (IsCurrentUserProfile,
                                     IsCurrentUserProfileOrReadOnly)
from account.api.serializers import (BasicPreferenceSerializer,
                                     CategoryPreferenceReadSerializer,
                                     ProfilePreferenceReadSerializer,
                                     ProfileSerializer,
                                     ThemePreferenceReadSerializer)
from account.models import (CategoryPreference, Profile, ProfilePreference,
                            ThemePreference)
from common.views import UrlMixin


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.with_rating().with_followers_count()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.with_rating().with_followers_count()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsCurrentUserProfileOrReadOnly)


class ProfileUrlMixin(UrlMixin):
    model_class = Profile


class ProfileFollowers(ProfileUrlMixin, generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.with_rating().with_followers_count() \
            .filter(profilepreference__subject_profile=self.profile,
                    profilepreference__display=True)


class BaseChangeBookmark(views.APIView):
    attr_name = None
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)

    def post(self, request, *args, **kwargs):
        bookmark, created = getattr(self, self.attr_name).bookmark_set \
            .get_or_create(profile=request.user.profile)
        if created:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        try:
            bookmark = getattr(self, self.attr_name).bookmark_set \
                .filter(profile=request.user.profile).get()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
