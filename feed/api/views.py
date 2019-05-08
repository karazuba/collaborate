from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.api.permissions import IsCurrentUserProfile
from account.api.views import ProfileUrlMixin
from feed.models import FeedArticle
from publication.api.filters import ArticleFilterSet
from publication.api.serializers import ArticleListSerializer


class BaseArticleFeed:
    serializer_class = ArticleListSerializer
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)
    filter_class = ArticleFilterSet


class AllFeed(ProfileUrlMixin, BaseArticleFeed, generics.ListAPIView):
    def get_queryset(self):
        return FeedArticle.objects.exclude_preferences(self.profile) \
            .with_rating().with_popularity()


class ProfileFollowFeed(ProfileUrlMixin, BaseArticleFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_profile_follows(profile).with_rating().with_popularity()


class TagFollowFeed(ProfileUrlMixin, BaseArticleFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_tag_follows(profile).with_rating().with_popularity()
