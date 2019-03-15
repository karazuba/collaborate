from django.urls import path, include

from . import views


urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>/', views.ArticleDetail.as_view(), name='article-detail'),
    path('articles/<int:pk>/vote/', views.ArticleVote.as_view()),
    path('articles/<int:article_pk>/comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('comments/<int:pk>/vote/', views.CommentVote.as_view()),
]
