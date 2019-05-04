from django_filters import rest_framework as filters

from account.models import Profile
from publication.models import Article, Category, Comment, Theme


class ArticleFilterSet(filters.FilterSet):
    author = filters.ModelChoiceFilter(field_name='author__profile',
                                       queryset=Profile.objects.all())
    categories = filters.ModelMultipleChoiceFilter(field_name='categories',
                                                   queryset=Category.objects.all(),
                                                   conjoined=True)
    themes = filters.ModelMultipleChoiceFilter(field_name='themes',
                                               queryset=Theme.objects.all(),
                                               conjoined=True)
    ordering = filters.OrderingFilter(
        fields=('creation_date', 'rating', 'popularity'))

    class Meta:
        model = Article
        fields = {
            'ordering': ['exact'],
            'author': ['exact'],
            'categories': ['exact'],
            'themes': ['exact'],
            'headline': ['icontains'],
            'creation_date': ['gt', 'lt'],
        }


class CommentFilterSet(filters.FilterSet):
    ordering = filters.OrderingFilter(fields=('creation_date', 'rating'))

    class Meta:
        model = Comment
        fields = ('ordering',)
