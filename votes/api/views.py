from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.api.permissions import IsCurrentUserProfile
from publication.api.views import ArticleUrlMixin, CommentUrlMixin
from votes.api.serializers import BasicVoteSerializer


class BaseMakeVote(views.APIView):
    attr_name = None
    permission_classes = (IsAuthenticated, IsCurrentUserProfile)

    def post(self, request, *args, **kwargs):
        serializer = BasicVoteSerializer(data=request.data)
        if serializer.is_valid():
            new_value = serializer.data['value']
            vote, created = getattr(self, self.attr_name).vote_set \
                .get_or_create(user=request.user,
                               defaults={'value': new_value})
            if not created and vote.value != new_value:
                vote.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakeArticleVote(ArticleUrlMixin, BaseMakeVote):
    pass


class MakeCommentVote(CommentUrlMixin, BaseMakeVote):
    pass
