from django_filters import rest_framework as filters

from publication import models


class ArticleFilter(filters.FilterSet):
    categories = filters.ModelMultipleChoiceFilter(field_name='categories',
                                                   queryset=models.Category.objects.all(),
                                                   conjoined=True)
    themes = filters.ModelMultipleChoiceFilter(field_name='themes',
                                               queryset=models.Theme.objects.all(),
                                               conjoined=True)

    class Meta:
        model = models.Article
        fields = {
            'author__username': ['exact'],
            'creation_date': ['exact', 'gt', 'lt'],
            'categories': ['exact'],
            'themes': ['exact'],
        }
