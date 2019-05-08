from django.urls import path

from accounts.api.views import ProfileDetail, ProfileFollowers, ProfileList

urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profiles/<int:pk>/', ProfileDetail.as_view()),
    path('profiles/<int:profile_pk>/followers/', ProfileFollowers.as_view()),
]
