from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from feed.models import FeedArticle
from publication.api.serializers import ArticleListSerializer
from publication.api.filters import ArticleFilterSet


class FollowFeed(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = ArticleFilterSet

    def get_queryset(self):
        profile = self.request.user.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_follows(profile).with_rating().with_popularity()


class InterestFeed(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = ArticleFilterSet

    def get_queryset(self):
        profile = self.request.user.profile
        return FeedArticle.objects.exclude_preferences(profile) \
            .filter_preferences(profile).with_rating().with_popularity()
