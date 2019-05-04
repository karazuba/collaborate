from django.urls import path

from account.api.views import (ProfileCategoryPreferences, ProfileDetail,
                               ProfileFollowers, ProfileFollows,
                               ProfileThemePreferences, ProfileList)

urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profiles/<int:pk>/', ProfileDetail.as_view()),
    path('profiles/<int:pk>/followers/', ProfileFollowers.as_view()),
    path('profiles/<int:pk>/follows/', ProfileFollows.as_view()),
    path('profiles/<int:pk>/preferences/themes/',
         ProfileThemePreferences.as_view()),
    path('profiles/<int:pk>/preferences/categories/',
         ProfileCategoryPreferences.as_view()),
]
