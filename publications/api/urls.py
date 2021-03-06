from django.urls import path

from publications.api.views import (ArticleDetail, ArticleList, CommentDetail,
                                    CommentsList)

urlpatterns = [
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>/', ArticleDetail.as_view()),
    path('articles/<int:article_pk>/comments/',
         CommentsList.as_view(), name='article-comment-list'),
    path('comments/<int:pk>/', CommentDetail.as_view()),
]
