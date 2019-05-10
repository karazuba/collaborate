from django.urls import path

from tags.api.views import ThemeList, CategoryList

urlpatterns = [
    path('themes/', ThemeList.as_view()),
    path('categories/', CategoryList.as_view()),
]
