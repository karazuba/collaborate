import pytest
from model_mommy import mommy

from feed.models import FeedArticle


@pytest.mark.django_db
class TestArticleFeedModel:

    def test_exclude_preferences(self, profile_factory):
        profile = profile_factory.get()

        articles = []

        theme = mommy.make('tags.Theme')
        profile.themepreference_set.create(theme=theme, display=False)
        article = mommy.make(FeedArticle, author=profile)
        article.themes.add(theme)
        articles.append(article)

        category = mommy.make('tags.Category')
        profile.categorypreference_set.create(category=category, display=False)
        article = mommy.make(FeedArticle, author=profile)
        article.categories.add(category)
        articles.append(article)

        another_profile = profile_factory.get()
        profile.profilepreference_set.create(subject_profile=another_profile,
                                             display=False)
        article = mommy.make(FeedArticle, author=another_profile)
        articles.append(article)

        for a in articles:
            assert a in FeedArticle.objects.all()
            assert a not in FeedArticle.objects.exclude_preferences(profile)

        article = mommy.make(FeedArticle, author=profile)
        assert article in FeedArticle.objects.exclude_preferences(profile)

    def test_filter_tag_follows(self, profile_factory):
        profile = profile_factory.get()
        theme = mommy.make('tags.Theme')
        category = mommy.make('tags.Category')
        profile.themepreference_set.create(theme=theme, display=True)
        profile.categorypreference_set.create(category=category, display=True)

        articles = []

        article = mommy.make(FeedArticle, author=profile)
        article.themes.add(theme)
        articles.append(article)

        article = mommy.make(FeedArticle, author=profile)
        article.categories.add(category)
        articles.append(article)

        article = mommy.make(FeedArticle, author=profile)
        article.themes.add(theme)
        article.categories.add(category)
        articles.append(article)

        for a in articles:
            assert a in FeedArticle.objects.filter_tag_follows(profile)

        article = mommy.make(FeedArticle, author=profile)
        assert article not in FeedArticle.objects.filter_tag_follows(profile)

    def test_filter_profile_follows(self, profile_factory):
        profile = profile_factory.get()
        another_profile = profile_factory.get()
        profile.profilepreference_set.create(subject_profile=another_profile,
                                             display=True)

        article = mommy.make(FeedArticle, author=another_profile)

        assert article in FeedArticle.objects.filter_profile_follows(profile)

        article = mommy.make(FeedArticle, author=profile)

        assert article not in FeedArticle.objects. \
            filter_profile_follows(profile)
