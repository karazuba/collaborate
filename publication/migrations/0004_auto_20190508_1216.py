# Generated by Django 2.2 on 2019-05-08 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0003_auto_20190507_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='creation_date',
            new_name='creation_datetime',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='update_date',
            new_name='update_datetime',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='creation_date',
            new_name='creation_datetime',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='update_date',
            new_name='update_datetime',
        ),
        migrations.AlterModelTable(
            name='articlevote',
            table='publication_article_votes',
        ),
        migrations.AlterModelTable(
            name='commentvote',
            table='publication_comment_votes',
        ),
    ]
