import pytest
from model_mommy import mommy

from preferences.models import ThemePreference
from recommendations.services import ThemeRecommendationService


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

        qs = ThemePreference.objects.all()
        recommendations = ThemeRecommendationService(qs).recommend()

        for p, t in match:
            assert t.id in map(lambda r: r[0], recommendations[p.id])
        for p, t in mismatch:
            assert t.id not in map(lambda r: r[0], recommendations[p.id])
