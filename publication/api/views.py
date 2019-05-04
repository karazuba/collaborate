from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from publication.api.filters import ArticleFilterSet, CommentFilterSet
from publication.api.permissions import IsAuthorOrReadOnly
from publication.api.serializers import (ArticleListSerializer,
                                         ArticleReadSerializer,
                                         ArticleWriteSerializer,
                                         CategorySerializer,
                                         CommentCreateSerializer,
                                         CommentSerializer, ThemeSerializer,
                                         VoteSerializer)
from publication.models import Article, Category, Comment, Theme


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.with_rating()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = ArticleFilterSet

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleWriteSerializer
        return ArticleListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.with_rating()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleWriteSerializer
        return ArticleReadSerializer


class ArticleMixin:
    article_url_kwarg = 'article_pk'

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
        self.article = None

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        if self.article_url_kwarg in self.kwargs:
            article_pk = self.kwargs[self.article_url_kwarg]
            self.article = get_object_or_404(Article, pk=article_pk)

        return request

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['article'] = self.article
        return context


class CommentsList(ArticleMixin, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = CommentFilterSet

    def get_queryset(self):
        queryset = Comment.objects.filter(article=self.article).with_rating()
        parent_id = self.request.query_params.get('parent_id', None)
        queryset = queryset.filter(parent_id=parent_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.with_rating()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class BaseVote(views.APIView):
    model = None
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            new_value = serializer.data['value']
            vote, created = obj.vote_set.get_or_create(user=request.user,
                                                       defaults={'value': new_value})
            if not created and vote.value != new_value:
                vote.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleVote(BaseVote):
    model = Article


class CommentVote(BaseVote):
    model = Comment


class ThemeList(generics.ListCreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
