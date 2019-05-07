from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from feed.models import FeedArticle
from publication.api.filters import ArticleFilterSet
from publication.api.serializers import ArticleListSerializer


class BaseFeed:
    serializer_class = ArticleListSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = ArticleFilterSet


class AllFeed(BaseFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.request.user.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .with_rating().with_popularity()


class ProfileFollowFeed(BaseFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.request.user.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_profile_follows(profile).with_rating().with_popularity()


class TagFollowFeed(BaseFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.request.user.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_tag_follows(profile).with_rating().with_popularity()
