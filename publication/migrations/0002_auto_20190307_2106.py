# Generated by Django 2.1.7 on 2019-03-07 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='publication.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.CharField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='article',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_set', related_query_name='reply', to='publication.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
