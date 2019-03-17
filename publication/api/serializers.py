from rest_framework import serializers

from publication import models


class BasePublicationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return getattr(obj, 'rating', None)


class ArticleListSerializer(BasePublicationSerializer):
    class Meta:
        model = models.Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'rating',  'author', 'categories', 'creation_date')


class ArticleDetailSerializer(BasePublicationSerializer):
    class Meta:
        model = models.Article
        fields = ('id', 'headline', 'thumbnail', 'description', 'body', 'rating',
                  'author', 'themes', 'categories', 'creation_date', 'update_date')


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ('id', 'headline', 'thumbnail', 'description',
                  'body', 'themes', 'categories')


class CommentSerializer(BasePublicationSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'article', 'parent', 'author', 'rating', 'body',
                  'creation_date', 'update_date')
        read_only_fields = ('article', 'parent')


class CommentCreateSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Comment.objects.all(), required=False)

    def validate_parent(self, parent):
        if models.Comment.objects.get(pk=parent.id).article_id != self.context['article_id']:
            raise serializers.ValidationError(
                "The parent comment must belong to the current article")
        return parent

    class Meta:
        model = models.Comment
        fields = ('id', 'parent', 'body')


class VoteSerializer(serializers.Serializer):
    value = serializers.BooleanField()


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Theme
        fields = ('id', 'label', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'label', 'description')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Profile
        fields = ('id', 'user', 'bio', 'followers_count',
                  'article_rating', 'comment_rating')


class ProfileFollowSerializer(serializers.Serializer):
    to_profile = serializers.IntegerField(required=True)

    def validate_to_profile(self, to_profile):
        if not models.Profile.objects.filter(pk=to_profile).exists():
            raise serializers.ValidationError(
                "This field must be assosiated with an existing user")
        return to_profile


class ThemePreferenceSerializer(serializers.ModelSerializer):
    theme_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Theme.objects.all())

    class Meta:
        model = models.ThemePreference
        fields = ('theme_id', 'display', 'profile')
        read_only_fields = ('profile',)


class CategoryPreferenceSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all())

    class Meta:
        model = models.CategoryPreference
        fields = ('category_id', 'display', 'profile')
        read_only_fields = ('profile',)
