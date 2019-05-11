from collections import defaultdict

import pandas as pd
from django.db import transaction
from surprise import SVD, Dataset, Reader

from recommendations.models import ThemeRecommendation
from preferences.models import ThemePreference


TOP_PREDICTIONS_NUMBER = 5


def _load_data():
    qs = ThemePreference.objects.all()
    df = pd.DataFrame(qs.values())

    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(
        df[['profile_id', 'theme_id', 'display']], reader)

    return data


def _train(trainset):
    algorithm = SVD()
    algorithm.fit(trainset)
    return algorithm


def _predict(algorithm, testset):
    predictions = defaultdict(list)
    for profile_id, theme_id, true_rating, estimate, _ in algorithm.test(testset):
        predictions[profile_id].append((theme_id, estimate))
    return predictions


def _get_top_predictions(predictions):
    top_predictions = defaultdict(list)
    for profile_id, ratings in predictions.items():
        ratings.sort(key=lambda r: r[1], reverse=True)
        top_predictions[profile_id] = ratings[:TOP_PREDICTIONS_NUMBER]
    return top_predictions


def _refresh_recommendations(profile_id, recommendations):
    ThemePreference.objects.filter(profile_id=profile_id).delete()
    for r in recommendations:
        ThemeRecommendation.objects.create(profile_id=profile_id,
                                           theme_id=r[0],
                                           estimated_rating=r[1])


@transaction.atomic
def recommendation_task():
    data = _load_data()
    trainset = data.build_full_trainset()

    algorithm = _train(trainset)

    testset = trainset.build_anti_testset()
    predictions = _predict(algorithm, testset)
    top_predictions = _get_top_predictions(predictions)

    for profile_id, ratings in top_predictions.items():
        recommendations = (r for r in ratings if r[1] > 0.5)
        _refresh_recommendations(profile_id, recommendations)
