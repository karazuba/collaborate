from django.urls import path

from feed.api.views import FollowFeed, InterestFeed

urlpatterns = [
    path('feed/follows/', FollowFeed.as_view()),
    path('feed/interests/', InterestFeed.as_view()),
]
