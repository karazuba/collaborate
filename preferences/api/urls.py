from django.urls import path

from preferences.api.views import (CategoryPreferenceList,
                                   ChangeCategoryPreference,
                                   ChangeProfilePreference,
                                   ChangeThemePreference,
                                   ProfilePreferenceList, ThemePreferenceList)

urlpatterns = [
    path('profiles/<int:profile_pk>/preferences/themes/',
         ThemePreferenceList.as_view()),
    path('profiles/<int:profile_pk>/preferences/categories/',
         CategoryPreferenceList.as_view()),
    path('profiles/<int:profile_pk>/preferences/profiles/',
         ProfilePreferenceList.as_view()),
    path('profiles/<int:pk>/preferences/themes/<int:theme_pk>/',
         ChangeThemePreference.as_view()),
    path('profiles/<int:pk>/preferences/categories/<int:category_pk>/',
         ChangeCategoryPreference.as_view()),
    path('profiles/<int:pk>/preferences/profiles/<int:profile_pk>/',
         ChangeProfilePreference.as_view()),
]
