from django.urls import path, include

from . import views


urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>/', views.ArticleDetail.as_view(), name='article-detail'),
    path('articles/<int:pk>/vote/', views.ArticleVote.as_view()),
    path('articles/<int:article_pk>/comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('comments/<int:pk>/vote/', views.CommentVote.as_view()),
    path('themes/', views.ThemeList.as_view(), name='theme-list'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/followers/', views.ProfileFollowers.as_view()),
    path('profiles/<int:pk>/follows/', views.ProfileFollows.as_view()),
    path('profiles/<int:pk>/preferences/themes/',
         views.ProfileThemePreferences.as_view()),
    path('profiles/<int:pk>/preferences/categories/',
         views.ProfileCategoryPreferences.as_view()),
]
