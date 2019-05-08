from rest_framework import generics, status, views
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from account.api.permissions import IsCurrentUserProfile
from common.views import UrlMixin
from publication.api.filters import ArticleFilterSet, CommentFilterSet
from publication.api.permissions import IsAuthorOrReadOnly
from publication.api.serializers import (ArticleListSerializer,
                                         ArticleReadSerializer,
                                         ArticleWriteSerializer,
                                         BasicVoteSerializer,
                                         CategorySerializer,
                                         CommentCreateSerializer,
                                         CommentSerializer, ThemeSerializer)
from publication.models import Article, Category, Comment, Theme


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.with_rating().with_popularity()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = ArticleFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleListSerializer
        return ArticleWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.with_rating()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleReadSerializer
        return ArticleWriteSerializer


class ArticleUrlMixin(UrlMixin):
    model_class = Article


class CommentsList(ArticleUrlMixin, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = CommentFilterSet

    def get_queryset(self):
        queryset = Comment.objects.filter(article=self.article).with_rating()
        parent_id = self.request.query_params.get('parent_id', None)
        queryset = queryset.filter(parent_id=parent_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.with_rating()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


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


class CommentUrlMixin(UrlMixin):
    model_class = Comment


class MakeCommentVote(CommentUrlMixin, BaseMakeVote):
    pass


class ThemeList(generics.ListCreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ThemeUrlMixin(UrlMixin):
    model_class = Theme


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUrlMixin(UrlMixin):
    model_class = Category
