from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import api_root
from .publication.views import ArticleList, ArticleDetail, CommentList, CommentDetail, ArticleVote, CommentVote


urlpatterns = [
    path('article/', ArticleList.as_view(), name='article-list'),
    path('article/<int:pk>', ArticleDetail.as_view(), name='article-detail'),
    path('article/<int:pk>/vote', ArticleVote.as_view()),
    path('article/<int:article_pk>/comments/',
         CommentList.as_view()),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment-detail'),
    path('comment/<int:pk>/vote', CommentVote.as_view()),
    path('', api_root),
]

urlpatterns = format_suffix_patterns(urlpatterns)
