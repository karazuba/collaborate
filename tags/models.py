from django.db import models


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
