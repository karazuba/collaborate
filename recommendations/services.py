from collections import defaultdict

import pandas as pd
from django.db import transaction
from surprise import SVD, Dataset, Reader


class ThemeRecommendationService:
    def __init__(self, queryset):
        df = pd.DataFrame(queryset.values())
        reader = Reader(rating_scale=(0, 1))
        data = Dataset.load_from_df(
            df[['profile_id', 'theme_id', 'display']], reader)
        self.data = data

    def __train(self, trainset):
        algorithm = SVD()
        algorithm.fit(trainset)
        return algorithm

    def recommend(self):
        trainset = self.data.build_full_trainset()
        algorithm = self.__train(trainset)

        testset = trainset.build_anti_testset()
        predictions = algorithm.test(testset)

        recommendations = defaultdict(list)
        for profile_id, theme_id, true_rating, estimate, _ in predictions:
            if estimate > 0.5:
                recommendations[profile_id].append((theme_id, estimate))
        return recommendations


def get_top_predictions(predictions, n=5):
    top = defaultdict(list)
    for profile_id, ratings in predictions.items():
        ratings.sort(key=lambda r: r[1], reverse=True)
        top[profile_id] = ratings[:n]
    return top
