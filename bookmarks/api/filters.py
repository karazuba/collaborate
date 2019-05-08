from django_filters import rest_framework as filters

from bookmarks.models import ArticleBookmark


class ArticleBookmarkFilterSet(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(('added_datetime', 'date'),)
    )

    class Meta:
        model = ArticleBookmark
        fields = ('ordering',)
