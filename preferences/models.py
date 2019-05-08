from django.db import models


class BasePreference(models.Model):
    display = models.BooleanField()
    profile = models.ForeignKey(to='account.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.id)} {str(self.display)} {str(self.profile)}'

    class Meta:
        abstract = True


class ThemePreference(BasePreference):
    theme = models.ForeignKey(to='publication.Theme', on_delete=models.CASCADE,
                              related_name='preference_set',
                              related_query_name='preference')

    def __str__(self):
        return f'{super().__str__()} {str(self.theme)}'

    class Meta:
        db_table = 'theme_preferences'
        unique_together = ('profile', 'theme')


class CategoryPreference(BasePreference):
    category = models.ForeignKey(to='publication.Category', on_delete=models.CASCADE,
                                 related_name='preference_set',
                                 related_query_name='preference')

    def __str__(self):
        return f'{super().__str__()} {str(self.category)}'

    class Meta:
        db_table = 'category_preferences'
        unique_together = ('profile', 'category')


class ProfilePreference(BasePreference):
    subject_profile = models.ForeignKey(to='account.Profile', on_delete=models.CASCADE,
                                        related_name='preference_set',
                                        related_query_name='preference')

    def __str__(self):
        return f'{super().__str__()} {str(self.subject_profile)}'

    class Meta:
        db_table = 'profile_preferences'
        unique_together = ('profile', 'subject_profile')
