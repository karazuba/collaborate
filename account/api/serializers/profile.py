from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'bio', 'followers_count',
                  'article_rating', 'comment_rating')
        read_only_fields = ('id', 'username', 'followers_count',
                            'article_rating', 'comment_rating')


class ProfileFollowSerializer(serializers.Serializer):
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all())
