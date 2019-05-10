from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.api.permissions import IsCurrentUserProfile
from accounts.api.views import ProfileUrlMixin
from feed.models import FeedArticle
from publications.api.filters import ArticleFilterSet
from publications.api.serializers import ArticleListSerializer


class BaseArticleFeed(ProfileUrlMixin):
    url_kwarg = 'pk'
    serializer_class = ArticleListSerializer
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)
    filter_class = ArticleFilterSet


class AllArticleFeed(BaseArticleFeed, generics.ListAPIView):
    def get_queryset(self):
        return FeedArticle.objects.exclude_preferences(self.profile) \
            .with_rating().with_popularity()


class ProfileFollowArticleFeed(BaseArticleFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_profile_follows(profile).with_rating().with_popularity()


class TagFollowArticleFeed(BaseArticleFeed, generics.ListAPIView):
    def get_queryset(self):
        profile = self.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_tag_follows(profile).with_rating().with_popularity()
