from django.db.models import Q, Subquery

from publications.models import Article, ArticleQuerySet


class ArticleFeedQuerySet(ArticleQuerySet):
    def exclude_preferences(self, profile):
        ignored_themes = Q(themes__preference__profile=profile,
                           themes__preference__display=False)
        ignored_categories = Q(categories__preference__profile=profile,
                               categories__preference__display=False)
        ignored_profiles = Q(author__preference__profile=profile,
                             author__preference__display=False)
        return self.exclude(ignored_themes) \
            .exclude(ignored_categories) \
            .exclude(ignored_profiles)

    def filter_profile_follows(self, profile):
        folowed_profiles = Q(author__preference__profile=profile,
                             author__preference__display=True)
        return self.filter(folowed_profiles)

    def filter_tag_follows(self, profile):
        followed_themes = Q(themes__preference__profile=profile,
                            themes__preference__display=True)
        followed_categories = Q(categories__preference__profile=profile,
                                categories__preference__display=True)
        return self.filter(followed_themes | followed_categories)


class FeedArticle(Article):
    objects = ArticleFeedQuerySet.as_manager()

    class Meta:
        proxy = True
