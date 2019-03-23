from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .. import models
from . import serializers
from . import permissions
from . import filters


class BaseFeed:
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.ArticleFilter
    ordering_fields = ('creation_date', 'rating', 'popularity')
    ordering = ('-popularity',)


class ArticleList(BaseFeed, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        qs = models.Article.objects.with_rating().with_popularity()
        if hasattr(self.request.user, 'profile'):
            qs = qs.exclude_preferences(self.request.user.profile)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ArticleCreateSerializer
        return serializers.ArticleListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ArticleDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAuthorOrReadOnly)

    def get_queryset(self):
        return models.Article.objects.with_rating()


class ArticleComments(views.APIView):
    filter_backends = (OrderingFilter,)
    ordering_fields = ('creation_date', 'rating')
    ordering = ('-rating',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=kwargs['pk'])
        parent_id = self.request.query_params.get('parent_id', None)
        queryset = models.Comment.objects.filter(article=article,
                                                 parent_id=parent_id).with_rating()
        serializer = serializers.CommentSerializer(queryset, many=True,
                                                   context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(models.Article, pk=kwargs['pk'])
        serializer = serializers.CommentCreateSerializer(data=request.data,
                                                         context={'article_id': article.id})
        if serializer.is_valid():
            serializer.save(author=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsAuthorOrReadOnly)

    def get_queryset(self):
        return models.Comment.objects.with_rating()


class BaseVote(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        serializer = serializers.VoteSerializer(data=request.data)
        if serializer.is_valid():
            new_value = serializer.data['value']
            vote, created = obj.vote_set.get_or_create(user=request.user,
                                                       defaults={'value': new_value})
            if not created and vote.value != new_value:
                vote.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleVote(BaseVote):
    model = models.Article


class CommentVote(BaseVote):
    model = models.Comment


class ThemeList(generics.ListCreateAPIView):
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryList(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsCurrentUserProfileOrReadOnly)


class ProfileFollowers(views.APIView):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        queryset = models.Profile.objects.filter(
            id__in=profile.follower_set.all())
        serializer = serializers.ProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class ProfileFollows(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsCurrentUserProfileOrReadOnly)

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        queryset = profile.follows
        serializer = serializers.ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        serializer = serializers.ProfileFollowSerializer(data=request.data)
        if serializer.is_valid():
            profile.follows.add(serializer.data['to_profile'])
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        serializer = serializers.ProfileFollowSerializer(data=request.data)
        if serializer.is_valid():
            profile.follows.remove(serializer.data['to_profile'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseProfilePreferences(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.IsCurrentUserProfileOrReadOnly)

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        queryset = self.model.objects.filter(profile=profile)
        serializer = self.serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            if not self.value_model.objects.filter(preference__profile=profile).exists():
                self.model.objects.create(profile=profile, **serializer.data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, pk=kwargs['pk'])
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            self.model.objects.filter(profile=profile,
                                      **serializer.data).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileThemePreferences(BaseProfilePreferences):
    model = models.ThemePreference
    value_model = models.Theme
    serializer = serializers.ThemePreferenceSerializer


class ProfileCategoryPreferences(BaseProfilePreferences):
    model = models.CategoryPreference
    value_model = models.Category
    serializer = serializers.CategoryPreferenceSerializer


class FollowFeed(BaseFeed, generics.ListAPIView):
    ordering = ('creation_date',)
    serializer_class = serializers.ArticleListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        profile = self.request.user.profile
        return models.Article.objects.exclude_preferences(profile) \
            .filter_follows(profile).with_rating().with_popularity()


class InterestFeed(BaseFeed, generics.ListAPIView):
    serializer_class = serializers.ArticleListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        profile = self.request.user.profile
        return models.Article.objects.exclude_preferences(profile) \
            .filter_preferences(profile).with_rating().with_popularity()
