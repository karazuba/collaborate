from django.urls import path

from publication.api.views import (ArticleDetail, ArticleList, CategoryList,
                                   ChangeCategoryPreference,
                                   ChangeThemePreference, CommentDetail,
                                   CommentsList, MakeArticleVote,
                                   MakeCommentVote, ThemeList)

urlpatterns = [
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>/', ArticleDetail.as_view()),
    path('articles/<int:article_pk>/vote/', MakeArticleVote.as_view()),
    path('articles/<int:article_pk>/comments/', CommentsList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('comments/<int:comment_pk>/vote/', MakeCommentVote.as_view()),
    path('themes/', ThemeList.as_view()),
    path('themes/<int:theme_pk>/preference/', ChangeThemePreference.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:category_pk>/preference/',
         ChangeCategoryPreference.as_view()),
]
