from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.permissions import IsCurrentUserProfile
from accounts.api.views import ProfileUrlMixin
from bookmarks.api.filters import ArticleBookmarkFilterSet
from bookmarks.api.serializers import ArticleBookmarkReadSerializer
from bookmarks.models import ArticleBookmark
from publications.api.views import ArticleUrlMixin


class BaseChangeBookmark(views.APIView):
    attr_name = None
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)

    def post(self, request, *args, **kwargs):
        bookmark, created = getattr(self, self.attr_name).bookmark_set \
            .get_or_create(profile=request.user.profile,
                           defaults={'profile': request.user.profile})
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


class ChangeArticleBookmark(ArticleUrlMixin, BaseChangeBookmark):
    pass


class ArticleBookmarkList(ProfileUrlMixin, generics.ListAPIView):
    url_kwarg = 'pk'
    serializer_class = ArticleBookmarkReadSerializer
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)
    filterset_class = ArticleBookmarkFilterSet

    def get_queryset(self):
        return ArticleBookmark.objects.filter(profile=self.profile)
