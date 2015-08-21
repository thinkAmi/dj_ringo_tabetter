from django.db import models

class Tweets(models.Model):
    '''リンゴに関係するツイートを持つModel'''
    name = models.CharField('リンゴ名', max_length=255)
    tweet_id = models.BigIntegerField('Tweet ID')
    tweet = models.CharField('ツイート内容', max_length=255)
    tweeted_at = models.DateTimeField('ツイート日時')


class LastSearch(models.Model):
    '''前回検索時の情報を持たせておくModel'''
    prev_since_id = models.BigIntegerField('前回検索時のsince_id')