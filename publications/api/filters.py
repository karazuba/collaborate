from django_filters import rest_framework as filters

from accounts.models import Profile
from publications.models import Article, Comment
from tags.models import Theme, Category


class ArticleFilterSet(filters.FilterSet):
    categories = filters.ModelMultipleChoiceFilter(field_name='categories',
                                                   queryset=Category.objects.all(),
                                                   conjoined=True)
    themes = filters.ModelMultipleChoiceFilter(field_name='themes',
                                               queryset=Theme.objects.all(),
                                               conjoined=True)
    created = filters.DateFromToRangeFilter(field_name='creation_datetime')
    headline = filters.CharFilter(lookup_expr='icontains')
    ordering = filters.OrderingFilter(
        fields=('creation_datetime', 'rating', 'popularity'))

    class Meta:
        model = Article
        fields = ('ordering', 'author', 'categories', 'themes',  'headline', 'created')


class CommentFilterSet(filters.FilterSet):
    ordering = filters.OrderingFilter(fields=('creation_datetime', 'rating'))

    class Meta:
        model = Comment
        fields = ('ordering',)
