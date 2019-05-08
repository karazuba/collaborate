from django.db import models


class BaseVote(models.Model):
    value = models.BooleanField()
    profile = models.ForeignKey(to='account.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.id)} {str(self.value)} {str(self.profile)}'

    class Meta:
        abstract = True


class ArticleVote(BaseVote):
    article = models.ForeignKey(to='publication.Article', on_delete=models.CASCADE,
                                related_name='vote_set',
                                related_query_name='vote')

    def __str__(self):
        return f'{super().__str__()} {str(self.article)}'

    class Meta:
        db_table = 'article_votes'
        unique_together = ('profile', 'article')


class CommentVote(BaseVote):
    comment = models.ForeignKey(to='publication.Comment', on_delete=models.CASCADE,
                                related_name='vote_set',
                                related_query_name='vote')

    def __str__(self):
        return f'{super().__str__()} {str(self.comment)}'

    class Meta:
        db_table = 'comment_votes'
        unique_together = ('profile', 'comment')
