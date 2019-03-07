from django.db import models
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


class BasePreference(models.Model):
    display = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (str(self.id), str(self.display), str(self.user))

    class Meta:
        abstract = True


class ThemePreference(BasePreference):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE,
                              related_name='preference_set', related_query_name='preference')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.theme))

    class Meta:
        db_table = 'publication_theme_preference'
        unique_together = ('user', 'theme')


class CategoryPreference(BasePreference):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='preference_set', related_query_name='preference')

    def __str__(self):
        return '%s %s' % (super().__str__(), str(self.category))

    class Meta:
        db_table = 'publication_category_preference'
        unique_together = ('user', 'category')
