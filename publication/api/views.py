from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from common.views import UrlMixin
from publication.api.filters import ArticleFilterSet, CommentFilterSet
from publication.api.permissions import IsAuthorOrReadOnly
from publication.api.serializers import (ArticleListSerializer,
                                         ArticleReadSerializer,
                                         ArticleWriteSerializer,
                                         CommentCreateSerializer,
                                         CommentSerializer)
from publication.models import Article, Comment


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


class CommentUrlMixin(UrlMixin):
    model_class = Comment
