import pytest
from model_mommy import mommy

from publications.models import Article, Comment


@pytest.mark.django_db
class TestArticleModel:

    def test_rating(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make(Article, author=profile)

        assert article.rating == 0

        vote = article.vote_set.create(value=True, profile=profile)
        assert article.rating == 1

        vote.value = False
        vote.save()
        assert article.rating == -1

    def test_popularity(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make(Article, author=profile)

        popularity = Article.objects.with_rating().with_popularity().get().popularity
        assert popularity == 0

        vote = article.vote_set.create(value=True, profile=profile)
        new_popularity = Article.objects.with_rating().with_popularity().get().popularity
        assert new_popularity > popularity
        popularity = new_popularity

        vote.value = False
        vote.save()
        new_popularity = Article.objects.with_rating().with_popularity().get().popularity
        assert new_popularity < popularity


@pytest.mark.django_db
class TestCommentModel:

    def test_rating(self, profile_factory):
        profile = profile_factory.get()
        article = mommy.make(Article, author=profile)
        comment = mommy.make(Comment, author=profile, article=article)

        assert comment.rating == 0

        vote = comment.vote_set.create(value=True, profile=profile)
        assert comment.rating == 1

        vote.value = False
        vote.save()
        assert comment.rating == -1
