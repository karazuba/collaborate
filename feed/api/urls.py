from django.urls import path

from feed.api.views import AllFeed, ProfileFollowFeed, TagFollowFeed

urlpatterns = [
    path('feed/all/', AllFeed.as_view()),
    path('feed/follows/tags/', TagFollowFeed.as_view()),
    path('feed/follows/profiles/', ProfileFollowFeed.as_view()),
]
