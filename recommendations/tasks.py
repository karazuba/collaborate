from celery import shared_task
from django.db import transaction

from preferences.models import ThemePreference
from recommendations.models import ThemeRecommendation
from recommendations.services import (ThemeRecommendationService,
                                      get_top_predictions)


@transaction.atomic
def refresh_theme_recommendations(profile_id, recommendations):
    ThemeRecommendation.objects.filter(profile_id=profile_id).delete()
    for r in recommendations:
        ThemeRecommendation.objects.create(profile_id=profile_id,
                                           theme_id=r[0],
                                           estimated_rating=r[1])


@shared_task
def recommend_themes():
    qs = ThemePreference.objects.all()
    service = ThemeRecommendationService(qs)

    recommendations = get_top_predictions(service.recommend())

    for profile_id, ratings in recommendations.items():
        refresh_theme_recommendations(profile_id, ratings)
