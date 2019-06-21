from django.urls import path


urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profiles/me/', ProfileCurrent.as_view()),
    path('profiles/<int:pk>/', ProfileDetail.as_view()),
    path('profiles/<int:profile_pk>/followers/', ProfileFollowers.as_view()),
]
