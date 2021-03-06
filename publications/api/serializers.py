from rest_framework import serializers

from accounts.api.serializers import ProfileSerializer
from common.serializers import CurrentValueDefault
from publications.models import Article, Comment
from tags.api.serializers import CategorySerializer, ThemeSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    themes = ThemeSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'rating',  'author', 'categories', 'themes', 'creation_datetime')
        read_only_fields = fields


class ArticleReadSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    themes = ThemeSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description', 'body', 'rating',
                  'author', 'categories', 'themes', 'creation_datetime', 'update_datetime')
        read_only_fields = fields


class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description', 'body',
                  'categories', 'themes', 'creation_datetime', 'update_datetime')


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article_id', 'parent_id', 'author', 'rating', 'body',
                  'creation_datetime', 'update_datetime')
        read_only_fields = ('id', 'article_id', 'parent_id', 'author', 'rating',
                            'creation_datetime', 'update_datetime')


class CurrentArticleDefault(CurrentValueDefault):
    key = 'article'


class CommentCreateSerializer(serializers.ModelSerializer):
    article = serializers.HiddenField(default=CurrentArticleDefault())
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), source='parent',
        required=False, allow_null=True,
        error_messages={
            'does_not_exist': 'There is no such comment in this article.'})

    class Meta:
        model = Comment
        fields = ('id', 'article', 'parent_id', 'body')

    def get_fields(self):
        fields = super().get_fields()

        qs = fields['parent_id'].queryset
        fields['parent_id'].queryset = qs.filter(
            article=self.context['article'])

        return fields
