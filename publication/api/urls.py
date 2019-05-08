from django.urls import path

from publication.api.views import (ArticleDetail, ArticleList, CategoryList,
                                   CommentDetail, CommentsList, ThemeList)

urlpatterns = [
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>/', ArticleDetail.as_view()),
    path('articles/<int:article_pk>/comments/', CommentsList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('themes/', ThemeList.as_view()),
    path('categories/', CategoryList.as_view()),
]
