from django.db import models
from django.db.models import Q, Count
from django.contrib.auth.models import User

from .classification import Theme, Category


class PublicationQuerySet(models.QuerySet):
    def with_rating(self):
        upvotes = Count('vote', filter=Q(vote__value=True))
        downvotes = Count('vote', filter=Q(vote__value=False))
        return self.annotate(rating=upvotes-downvotes)


class BasePublication(models.Model):
    body = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = PublicationQuerySet.as_manager()

    def __str__(self):
        return '%s %s' % (str(self.id), str(self.author))

    class Meta:
        abstract = True


class Article(BasePublication):
    headline = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=350, blank=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/%Y/%m/%d/', null=True, blank=True)
    themes = models.ManyToManyField(Theme)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return '%s %s' % (super().__str__(), self.headline)


class Comment(BasePublication):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                               related_name='reply_set', related_query_name='reply')

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
                                related_name='vote_set', related_query_name='vote')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.article))

    class Meta:
        db_table = 'publication_article_vote'
        unique_together = ('user', 'article')


class CommentVote(BaseVote):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='vote_set', related_query_name='vote')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.comment))

    class Meta:
        db_table = 'publication_comment_vote'
        unique_together = ('user', 'comment')
