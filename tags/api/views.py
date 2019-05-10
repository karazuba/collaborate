from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from common.views import UrlMixin
from tags.api.serializers import CategorySerializer, ThemeSerializer
from tags.models import Category, Theme


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
