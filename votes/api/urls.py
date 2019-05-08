from django.urls import path

from votes.api.views import MakeCommentVote, MakeArticleVote

urlpatterns = [
    path('profiles/<int:pk>/votes/comments/<int:comment_pk>/',
         MakeCommentVote.as_view()),
    path('profiles/<int:pk>/votes/articles/<int:article_pk>/',
         MakeArticleVote.as_view()),
]
