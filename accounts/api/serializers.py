from rest_framework import serializers

from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'bio', 'followers_count',
                  'article_rating', 'comment_rating')
        read_only_fields = ('id', 'username', 'followers_count',
                            'article_rating', 'comment_rating')
