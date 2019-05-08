# Generated by Django 2.2 on 2019-05-08 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_delete_articlebookmark'),
        ('publication', '0004_auto_20190508_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleBookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_datetime', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_set', related_query_name='bookmark', to='publication.Article')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
            ],
            options={
                'db_table': 'article_bookmarks',
                'unique_together': {('profile', 'article')},
            },
        ),
    ]
