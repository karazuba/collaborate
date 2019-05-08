from django.db.models import Subquery

from account.models import Profile
from publication.models import Article, ArticleQuerySet
from tags.models import Category, Theme


class FeedQuerySet(ArticleQuerySet):
    def exclude_preferences(self, profile):
        ignored_themes = Theme.objects.filter(preference__profile=profile,
                                              preference__display=False) \
            .values_list('id', flat=True)
        ignored_categories = Category.objects.filter(preference__profile=profile,
                                                     preference__display=False) \
            .values_list('id', flat=True)
        ignored_profiles = Profile.objects.filter(preference__profile=profile,
                                                  preference__display=False) \
            .values_list('id', flat=True)
        return self.exclude(themes__in=Subquery(ignored_themes)) \
            .exclude(categories__in=Subquery(ignored_categories)) \
            .exclude(author__profile__in=Subquery(ignored_profiles))

    def filter_profile_follows(self, profile):
        folowed_profiles = Profile.objects.filter(preference__profile=profile,
                                                  preference__display=True) \
            .values_list('id', flat=True)
        return self.filter(author__profile__in=folowed_profiles)

    def filter_tag_follows(self, profile):
        followed_themes = Theme.objects.filter(preference__profile=profile,
                                               preference__display=True) \
            .values_list('id', flat=True)
        followed_categories = Category.objects.filter(preference__profile=profile,
                                                      preference__display=True) \
            .values_list('id', flat=True)
        return self.filter(themes__in=Subquery(followed_themes),
                           categories__in=Subquery(followed_categories))


class FeedArticle(Article):
    objects = FeedQuerySet.as_manager()

    class Meta:
        proxy = True
