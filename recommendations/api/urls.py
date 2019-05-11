from django.urls import path

from recommendations.api.views import ThemeRecommendationList

urlpatterns = [
    path('profiles/<int:pk>/recommendations/themes/',
         ThemeRecommendationList.as_view())
]
