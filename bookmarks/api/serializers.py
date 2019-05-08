from rest_framework import serializers

from bookmarks.models import ArticleBookmark
from publications.api.serializers import ArticleReadSerializer

class ArticleBookmarkReadSerializer(serializers.ModelSerializer):
    article = ArticleReadSerializer()

    class Meta:
        model = ArticleBookmark
        fields = ('profile_id', 'article', 'added_datetime')
        read_only_fields = fields