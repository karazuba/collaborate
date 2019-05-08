from django.db import models


class BaseBookmark(models.Model):
    profile = models.ForeignKey(to='accounts.Profile',
                                on_delete=models.CASCADE)
    added_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.id)} {str(self.profile)}'

    class Meta:
        abstract = True


class ArticleBookmark(BaseBookmark):
    article = models.ForeignKey(to='publications.Article',
                                on_delete=models.CASCADE,
                                related_name='bookmark_set',
                                related_query_name='bookmark')

    def __str__(self):
        return f'{super().__str__()} {str(self.article)}'

    class Meta:
        db_table = 'article_bookmarks'
        unique_together = ('profile', 'article')
