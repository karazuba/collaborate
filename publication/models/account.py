from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User

from .publication import Theme, Category


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    follows = models.ManyToManyField('self', symmetrical=False,
                                     related_name='follower_set',
                                     related_query_name='follower')

    @property
    def article_rating(self):
        article_upvotes = Count('user__article__vote', distinct=True,
                                filter=Q(user__article__vote__value=True))
        article_downvotes = Count('user__article__vote', distinct=True,
                                  filter=Q(user__article__vote__value=False))
        return Profile.objects.filter(id=self.id).aggregate(article_rating=article_upvotes - article_downvotes)['article_rating']

    @property
    def comment_rating(self):
        comment_upvotes = Count('user__comment__vote', distinct=True,
                                filter=Q(user__comment__vote__value=True))
        comment_downvotes = Count('user__comment__vote', distinct=True,
                                  filter=Q(user__comment__vote__value=False))
        return Profile.objects.filter(id=self.id).aggregate(comment_rating=comment_upvotes-comment_downvotes)['comment_rating']

    @property
    def followers_count(self):
        return Profile.objects.filter(id=self.id).aggregate(followers_count=Count('follower', distinct=True))['followers_count']

    def __str__(self):
        return '%s %s' % (str(self.id), str(self.user))


class BasePreference(models.Model):
    display = models.BooleanField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (str(self.id), str(self.display), str(self.profile))

    class Meta:
        abstract = True


class ThemePreference(BasePreference):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE,
                              related_name='preference_set',
                              related_query_name='preference')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.theme))

    class Meta:
        db_table = 'publication_theme_preference'
        unique_together = ('profile', 'theme')


class CategoryPreference(BasePreference):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='preference_set',
                                 related_query_name='preference')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.category))

    class Meta:
        db_table = 'publication_category_preference'
        unique_together = ('profile', 'category')
