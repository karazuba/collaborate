from django.urls import path

from feed.api.views import (AllArticleFeed, ProfileFollowArticleFeed,
                            TagFollowArticleFeed)

urlpatterns = [
    path('profiles/<int:pk>/feed/articles/', AllArticleFeed.as_view()),
    path('profiles/<int:pk>/feed/tags/articles/',
         TagFollowArticleFeed.as_view()),
    path('profiles/<int:pk>/feed/profiles/articles/',
         ProfileFollowArticleFeed.as_view()),
]
