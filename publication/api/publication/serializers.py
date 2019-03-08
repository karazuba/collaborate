from rest_framework import serializers

from publication.models import Article, Comment


class BasePublicationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return getattr(obj, 'rating', None)


class ArticleListSerializer(BasePublicationSerializer):
    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'rating',  'author', 'categories', 'creation_date')


class ArticleDetailSerializer(BasePublicationSerializer):
    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description', 'body', 'rating',
                  'author', 'themes', 'categories', 'creation_date', 'update_date')


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'body', 'themes', 'categories')


class CommentSerializer(BasePublicationSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'article', 'parent', 'author', 'rating', 'body',
                  'creation_date', 'update_date')
        read_only_fields = ('article', 'parent')


class CommentCreateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False)

    def validate_parent(self, parent):
        if Comment.objects.get(pk=parent.id).article_id != self.context['article_id']:
            raise serializers.ValidationError(
                "The parent comment must belong to the current article")
        return parent

    class Meta:
        model = Comment
        fields = ('id', 'parent', 'body')
