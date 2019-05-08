from django.urls import path

from publication.api.views import (ArticleDetail, ArticleList, CategoryList,
                                   CommentDetail, CommentsList,
                                   MakeArticleVote, MakeCommentVote, ThemeList)

urlpatterns = [
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>/', ArticleDetail.as_view()),
    path('profiles/<int:pk>/votes/articles/<int:article_pk>/',
         MakeArticleVote.as_view()),
    path('articles/<int:article_pk>/comments/', CommentsList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('profiles/<int:pk>/votes/comments/<int:comment_pk>/',
         MakeCommentVote.as_view()),
    path('themes/', ThemeList.as_view()),
    path('categories/', CategoryList.as_view()),
]
