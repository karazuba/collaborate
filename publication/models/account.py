from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User


class ProfileQuerySet(models.QuerySet):
    def with_rating(self):

        article_upvotes = Count('user__article__vote',
                                filter=Q(user__article__vote__value=True),
                                distinct=True)
        article_downvotes = Count('user__article__vote',
                                  filter=Q(user__article__vote__value=False),
                                  distinct=True)
        comment_upvotes = Count('user__comment__vote',
                                filter=Q(user__comment__vote__value=True),
                                distinct=True)
        comment_downvotes = Count('user__comment__vote',
                                  filter=Q(user__comment__vote__value=False),
                                  distinct=True)
        return self.annotate(article_rating=article_upvotes-article_downvotes,
                             comment_rating=comment_upvotes-comment_downvotes)

    def with_followers_count(self):
        return self.annotate(followers=Count('follower', distinct=True))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    follows = models.ManyToManyField('self',
                                     symmetrical=False,
                                     related_name='follower_set',
                                     related_query_name='follower')

    objects = ProfileQuerySet.as_manager()

    def __str__(self):
        return '%s %s' % (str(self.id), str(self.user))
