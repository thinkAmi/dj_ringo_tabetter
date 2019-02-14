from django.db import models
from django.db.models.query import QuerySet


class Tweets(models.Model):
    """ リンゴに関係するツイートを持つModel """
    name = models.CharField('リンゴ名', max_length=255)
    tweet_id = models.BigIntegerField('Tweet ID')
    tweet = models.CharField('ツイート内容', max_length=255)
    tweeted_at = models.DateTimeField('ツイート日時')

    @classmethod
    def calculate_total_by_name(cls) -> QuerySet:
        """ リンゴ名ごとの全期間の合計数量 """
        return cls.objects.values('name').annotate(quantity=models.Count('name'))

    @classmethod
    def calculate_total_by_name_and_month(cls) -> QuerySet:
        """ リンゴ名ごと・月ごとの合計数量

            年は考慮せずに集約する
            (例) 2018年10月と2019年10月は、10月としてカウント

            PostgreSQLの関数を使っているため、SQLiteなどでは動作しない
        """
        return cls.objects.extra(select={'month': "date_part('month', tweeted_at)::int"}) \
                          .values('name', 'month') \
                          .annotate(quantity=models.Count('name')) \
                          .order_by('name', 'month')


class LastSearch(models.Model):
    """ 前回検索時の情報を持たせておくModel """
    prev_since_id = models.BigIntegerField('前回検索時のsince_id')
