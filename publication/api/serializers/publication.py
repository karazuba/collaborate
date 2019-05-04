from rest_framework import serializers

from account.api.serializers.profile import ProfileSerializer
from publication.api.serializers.tag import CategorySerializer, ThemeSerializer
from publication.models import Article, Comment


class BasePublicationSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(source='author.profile')
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return getattr(obj, 'rating', None)


class ArticleListSerializer(BasePublicationSerializer):
    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'rating',  'author', 'creation_date')
        read_only_fields = fields


class ArticleReadSerializer(BasePublicationSerializer):
    themes = ThemeSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description', 'body', 'rating',
                  'author', 'themes', 'categories', 'creation_date', 'update_date')
        read_only_fields = fields


class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'body', 'themes', 'categories')


class CommentSerializer(BasePublicationSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'article_id', 'parent_id', 'author', 'rating', 'body',
                  'creation_date', 'update_date')
        read_only_fields = ('id', 'article_id', 'parent_id', 'author', 'rating',
                            'creation_date', 'update_date')


class CurrentArticleDefault:
    def set_context(self, serializer_field):
        self.article = serializer_field.context['article']

    def __call__(self):
        return self.article

    def __repr__(self):
        return f'{self.__class__.__name__}()'


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
