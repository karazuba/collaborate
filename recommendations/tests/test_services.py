import pytest
from django.core.exceptions import ObjectDoesNotExist
from model_mommy import mommy

from recommendations.models import ThemeRecommendation
from recommendations.services import recommendation_task


@pytest.mark.django_db
class TestThemeRecommendationService:
    def test_recommendations(self, profile_factory):
        n = 48
        profiles = profile_factory.get(quantity=n)
        themes = mommy.make('tags.Theme', _quantity=n)

        # construct initial preferences so that each half of profiles
        # strictly prefer respective half of themes in contrast to another half
        for i, p in enumerate(profiles):
            for j, t in enumerate(themes):
                if i < n//2 and j < n//2 or i >= n//2 and j >= n//2:
                    t.preference_set.create(profile=p, display=True)
                else:
                    t.preference_set.create(profile=p, display=False)

        match = [
            [profiles[11], themes[8]],
            [profiles[38], themes[41]],
        ]
        mismatch = [
            [profiles[10], themes[39]],
            [profiles[47], themes[3]],
        ]

        for p, t in match + mismatch:
            t.preference_set.get(profile=p).delete()

        recommendation_task()

        for p, t in match:
            assert ThemeRecommendation.objects.filter(profile=p, theme=t).get()
        for p, t in mismatch:
            with pytest.raises(ObjectDoesNotExist):
                ThemeRecommendation.objects.filter(profile=p, theme=t).get()
