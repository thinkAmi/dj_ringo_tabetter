# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LastSearch',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('prev_since_id', models.BigIntegerField(verbose_name='前回検索時のsince_id')),
            ],
        ),
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='リンゴ名', max_length=255)),
                ('tweet_id', models.BigIntegerField(verbose_name='Tweet ID')),
                ('tweet', models.CharField(verbose_name='ツイート内容', max_length=255)),
                ('tweeted_at', models.DateTimeField(verbose_name='ツイート日時')),
            ],
        ),
    ]
