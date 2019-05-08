from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, ExpressionWrapper, F, Q
from django.db.models.functions import Cast, Now


class BaseTag(models.Model):
    label = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{str(self.id)} {self.label}'

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
        hours = Cast(Now() - F('creation_datetime'), models.FloatField()) \
            / 3600000000 + 1
        return self.annotate(popularity=ExpressionWrapper(F('rating')/hours,
                                                          output_field=models.FloatField()))


class CommentQuerySet(BasePublicationQuerySet):
    pass


class BasePublication(models.Model):
    body = models.TextField(blank=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(null=True, auto_now=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.id)} {str(self.author)}'

    class Meta:
        abstract = True


class Article(BasePublication):
    headline = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=350, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/%Y/%m/%d/',
                                  null=True, blank=True)
    themes = models.ManyToManyField(to=Theme)
    categories = models.ManyToManyField(to=Category)

    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return f'{super().__str__()} {self.headline}'


class Comment(BasePublication):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE,
                               null=True,
                               related_name='reply_set',
                               related_query_name='reply')

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return super().__str__()


class BaseVote(models.Model):
    value = models.BooleanField()
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.id)} {str(self.value)} {str(self.user)}'

    class Meta:
        abstract = True


class ArticleVote(BaseVote):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE,
                                related_name='vote_set',
                                related_query_name='vote')

    def __str__(self):
        return f'{super().__str__()} {str(self.article)}'

    class Meta:
        db_table = 'publication_article_votes'
        unique_together = ('user', 'article')


class CommentVote(BaseVote):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE,
                                related_name='vote_set',
                                related_query_name='vote')

    def __str__(self):
        return f'{super().__str__()} {str(self.comment)}'

    class Meta:
        db_table = 'publication_comment_votes'
        unique_together = ('user', 'comment')
