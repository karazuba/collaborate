from django.urls import path

from publication.api.views import (ArticleDetail, ArticleList, ArticleVote,
                                   CategoryList, CommentDetail, CommentsList,
                                   CommentVote, ThemeList)

urlpatterns = [
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>/', ArticleDetail.as_view()),
    path('articles/<int:pk>/vote/', ArticleVote.as_view()),
    path('articles/<int:article_pk>/comments/', CommentsList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('comments/<int:pk>/vote/', CommentVote.as_view()),
    path('themes/', ThemeList.as_view()),
    path('categories/', CategoryList.as_view()),
]
