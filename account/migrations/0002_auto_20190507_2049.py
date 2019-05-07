# Generated by Django 2.2 on 2019-05-07 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='follows',
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
                'db_table': 'account_profile_preference',
                'unique_together': {('profile', 'subject_profile')},
            },
        ),
    ]
