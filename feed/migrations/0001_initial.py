# Generated by Django 2.2 on 2019-05-03 20:24

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publication', '0002_auto_20190503_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedArticle',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('publication.article',),
        ),
    ]