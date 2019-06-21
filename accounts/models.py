from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Q


class ProfileQuerySet(models.QuerySet):
    article_upvotes = Count('article__vote', distinct=True,
                            filter=Q(article__vote__value=True))
    article_downvotes = Count('article__vote', distinct=True,
                              filter=Q(article__vote__value=False))

    article_rating = article_upvotes - article_downvotes

    comment_upvotes = Count('comment__vote', distinct=True,
                            filter=Q(comment__vote__value=True))
    comment_downvotes = Count('comment__vote', distinct=True,
                              filter=Q(comment__vote__value=False))

    comment_rating = comment_upvotes - comment_downvotes

    followers_count = Count('preference', distinct=True,
                            filter=Q(preference__display=True))

    def with_rating(self):
        return self.annotate(_article_rating=self.article_rating,
                             _comment_rating=self.comment_rating)

    def with_followers_count(self):
        return self.annotate(_followers_count=self.followers_count)


class Profile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)

    objects = ProfileQuerySet.as_manager()

    @property
    def article_rating(self):
        return getattr(self, '_article_rating', Profile.objects.filter(id=self.id)
                       .aggregate(article_rating=ProfileQuerySet.article_rating)['article_rating'])

    @property
    def comment_rating(self):
        return getattr(self, '_comment_rating', Profile.objects.filter(id=self.id)
                       .aggregate(comment_rating=ProfileQuerySet.comment_rating)['comment_rating'])

    @property
    def followers_count(self):
        return getattr(self, '_followers_count', Profile.objects.filter(id=self.id)
                       .aggregate(followers_count=ProfileQuerySet.followers_count)['followers_count'])

    def __str__(self):
        return f'{str(self.id)} {str(self.user)}'
