# Generated by Django 2.2 on 2019-05-08 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publication', '0004_auto_20190508_1216'),
        ('account', '0005_auto_20190508_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemePreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_set', related_query_name='preference', to='publication.Theme')),
            ],
            options={
                'db_table': 'theme_preferences',
                'unique_together': {('profile', 'theme')},
            },
        ),
        migrations.CreateModel(
            name='ProfilePreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
                ('subject_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_set', related_query_name='preference', to='account.Profile')),
            ],
            options={
                'db_table': 'profile_preferences',
                'unique_together': {('profile', 'subject_profile')},
            },
        ),
        migrations.CreateModel(
            name='CategoryPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference_set', related_query_name='preference', to='publication.Category')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Profile')),
            ],
            options={
                'db_table': 'category_preferences',
                'unique_together': {('profile', 'category')},
            },
        ),
    ]
