import pytest
from model_mommy import mommy

from accounts.models import Profile


@pytest.mark.django_db
class TestProfileModel:

    def test_rating(self, profile_factory):
        profile = profile_factory.get()

        assert profile.article_rating == 0
        assert profile.comment_rating == 0

        article = mommy.make('publications.Article', author=profile)
        comment = mommy.make('publications.Comment',
                             author=profile, article=article)

        article.vote_set.create(profile=profile, value=True)

        assert profile.article_rating == 1

        comment.vote_set.create(profile=profile, value=False)

        assert profile.comment_rating == -1

    def test_followers_count(self, profile_factory):
        profile = profile_factory.get()

        assert profile.followers_count == 0

        another_profile = profile_factory.get()
        another_profile.profilepreference_set \
            .create(subject_profile=profile, display=True)

        assert profile.followers_count == 1
