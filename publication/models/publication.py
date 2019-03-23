from django.db import models
from django.db.models import Q, Count, Subquery, F, ExpressionWrapper
from django.db.models.functions import Cast, Now
from django.contrib.auth.models import User


class BaseTag(models.Model):
    label = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s %s' % (str(self.id), self.label)

    class Meta:
        abstract = True


class Theme(BaseTag):
    pass


class Category(BaseTag):
    pass


class BasePublicationQuerySet(models.QuerySet):
    def with_rating(self):
        upvotes = Count('vote', filter=Q(vote__value=True))
        downvotes = Count('vote', filter=Q(vote__value=False))
        return self.annotate(rating=upvotes-downvotes)


class ArticleQuerySet(BasePublicationQuerySet):
    def with_popularity(self):
        hours = Cast(Now() - F('creation_date'), models.FloatField()) \
            / 3600000000 + 1
        return self.annotate(popularity=ExpressionWrapper(F('rating')/hours, output_field=models.FloatField()))

    def exclude_preferences(self, profile):
        ignored_themes = Theme.objects.filter(preference__profile=profile,
                                              preference__display=False) \
            .values_list('id', flat=True)
        ignored_categories = Category.objects.filter(preference__profile=profile,
                                                     preference__display=False) \
            .values_list('id', flat=True)
        return self.exclude(themes__in=Subquery(ignored_themes)) \
            .exclude(categories__in=Subquery(ignored_categories))

    def filter_follows(self, profile):
        return self.filter(author__profile__in=profile.follows.all())

    def filter_preferences(self, profile):
        followed_themes = Theme.objects.filter(preference__profile=profile,
                                               preference__display=True) \
            .values_list('id', flat=True)
        followed_categories = Category.objects.filter(preference__profile=profile,
                                                      preference__display=True) \
            .values_list('id', flat=True)
        return self.filter(themes__in=Subquery(followed_themes),
                           categories__in=Subquery(followed_categories))


class CommentQuerySet(BasePublicationQuerySet):
    pass


class BasePublication(models.Model):
    body = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (str(self.id), str(self.author))

    class Meta:
        abstract = True


class Article(BasePublication):
    headline = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=350, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d/',
                                  null=True, blank=True)
    themes = models.ManyToManyField(Theme)
    categories = models.ManyToManyField(Category)

    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return '%s %s' % (super().__str__(), self.headline)


class Comment(BasePublication):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                               related_name='reply_set',
                               related_query_name='reply')

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


class BaseVote(models.Model):
    value = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (str(self.id), str(self.value), str(self.user))

    class Meta:
        abstract = True


class ArticleVote(BaseVote):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='vote_set',
                                related_query_name='vote')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.article))

    class Meta:
        db_table = 'publication_article_vote'
        unique_together = ('user', 'article')


class CommentVote(BaseVote):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='vote_set',
                                related_query_name='vote')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.comment))

    class Meta:
        db_table = 'publication_comment_vote'
        unique_together = ('user', 'comment')
