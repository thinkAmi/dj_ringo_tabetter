# Generated by Django 4.1.1 on 2022-09-23 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_alter_lastsearch_id_alter_tweets_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='tweet_id',
            field=models.BigIntegerField(unique=True, verbose_name='Tweet ID'),
        ),
    ]