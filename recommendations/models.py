from django.db import models


class ThemeRecommendation(models.Model):
    profile = models.ForeignKey(to='accounts.Profile',
                                on_delete=models.Case)
    theme = models.ForeignKey(to='tags.Theme',
                              on_delete=models.CASCADE,
                              related_name='recommendation_set',
                              related_query_name='recommendation')
    estimated_rating = models.FloatField()

    def __str__(self):
        return f'{str(self.profile)} {str(self.theme)} {str(self.estimated_rating)}'

    class Meta:
        db_table = 'recommendation_themes'
        unique_together = ('profile', 'theme')
