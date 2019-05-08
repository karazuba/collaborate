from django.urls import path

from bookmarks.api.views import ArticleBookmarkList, ChangeArticleBookmark

urlpatterns = [
    path('profiles/<int:pk>/bookmarks/articles/', ArticleBookmarkList.as_view()),
    path('profiles/<int:pk>/bookmarks/articles/<int:article_pk>/',
         ChangeArticleBookmark.as_view()),
]
