from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from account.api.permissions import IsCurrentUserProfileOrReadOnly
from account.api.serializers import (CategoryPreferenceReadSerializer,
                                     CategoryPreferenceWriteSerializer,
                                     ProfileFollowSerializer,
                                     ProfileSerializer,
                                     ThemePreferenceReadSerializer,
                                     ThemePreferenceWriteSerializer)
from account.models import CategoryPreference, Profile, ThemePreference
from publication.models import Category, Theme


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsCurrentUserProfileOrReadOnly)


class ProfileFollowers(views.APIView):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        queryset = Profile.objects.filter(
            id__in=profile.follower_set.all())
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class ProfileFollows(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsCurrentUserProfileOrReadOnly)

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        queryset = profile.follows
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        serializer = ProfileFollowSerializer(data=request.data)
        if serializer.is_valid():
            profile.follows.add(serializer.data['profile_id'])
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        serializer = ProfileFollowSerializer(data=request.data)
        if serializer.is_valid():
            profile.follows.remove(serializer.data['profile_id'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseProfilePreferences(views.APIView):
    model_class = None
    value_model_class = None
    read_serializer_class = None
    write_serializer_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsCurrentUserProfileOrReadOnly)

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        queryset = self.model.objects.filter(profile=profile)
        serializer = self.read_serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        serializer = self.write_serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.value_model.objects.filter(preference__profile=profile).exists():
                self.model.objects.create(profile=profile, **serializer.data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        serializer = self.write_serializer_class(data=request.data)
        if serializer.is_valid():
            self.model.objects.filter(profile=profile,
                                      **serializer.data).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileThemePreferences(BaseProfilePreferences):
    model = ThemePreference
    value_model = Theme
    read_serializer_class = ThemePreferenceReadSerializer
    write_serializer_class = ThemePreferenceWriteSerializer


class ProfileCategoryPreferences(BaseProfilePreferences):
    model = CategoryPreference
    value_model = Category
    read_serializer_class = CategoryPreferenceReadSerializer
    write_serializer_class = CategoryPreferenceWriteSerializer
