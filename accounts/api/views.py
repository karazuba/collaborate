from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from accounts.api.permissions import IsCurrentUserProfileOrReadOnly
from accounts.api.serializers import ProfileSerializer
from accounts.models import Profile
from common.views import UrlMixin


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.with_rating().with_followers_count()
    serializer_class = ProfileSerializer


class ProfileCurrent(generics.RetrieveAPIView):
    queryset = Profile.objects.with_rating().with_followers_count()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


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
