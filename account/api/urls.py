from django.urls import path

from account.api.views import (CategoryPreferenceList, ProfileDetail,
                               ProfileFollowers, ProfileList,
                               ChangeProfilePreference, ProfilePreferenceList,
                               ThemePreferenceList)

urlpatterns = [
    path('profiles/', ProfileList.as_view()),
    path('profiles/<int:pk>/', ProfileDetail.as_view()),
    path('profiles/<int:profile_pk>/followers/', ProfileFollowers.as_view()),
    path('profiles/<int:profile_pk>/preference/', ChangeProfilePreference.as_view()),
    path('profiles/<int:profile_pk>/preferences/themes/',
         ThemePreferenceList.as_view()),
    path('profiles/<int:profile_pk>/preferences/categories/',
         CategoryPreferenceList.as_view()),
    path('profiles/<int:profile_pk>/preferences/profiles/',
         ProfilePreferenceList.as_view()),
]
