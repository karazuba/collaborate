from django.urls import path

from feed.api.views import AllFeed, ProfileFollowFeed, TagFollowFeed

urlpatterns = [
    path('profiles/<int:profile_pk>/feed/all/', AllFeed.as_view()),
    path('profiles/<int:profile_pk>/feed/follows/tags/', TagFollowFeed.as_view()),
    path('profiles/<int:profile_pk>/feed/follows/profiles/',
         ProfileFollowFeed.as_view()),
]
