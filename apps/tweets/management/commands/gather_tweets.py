from django.core.management.base import BaseCommand
import tweepy
from slacker import Slacker
import os
import re
import pytz
import traceback
from apps.tweets.models import Tweets, LastSearch
from libs.cultivars import Apple
from django.db import transaction

LOCAL_TIMEZONE = pytz.timezone('Asia/Tokyo')
# 一日に200ツイートはしないはず...
TWEET_COUNT = 200


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''manage.pyで使うときのエントリポイント'''
        self.cultivars = Apple().cultivars
        self.last_search = self.get_last_search()

        statuses = self.gather_tweets()
        if statuses:
            self.save_with_transaction(statuses)

        print('finish')


    def get_last_search(self):
        '''前回検索情報を取得する'''
        return LastSearch.objects.first()


    def gather_tweets(self):
        '''ツイートを取得し、idの降順にソートする'''
        # tweepyにて関連するツイートを取得
        try:
            auth = tweepy.AppAuthHandler(
                os.environ['TWITTER_CONSUMER_KEY'],
                os.environ['TWITTER_CONSUMER_SECRET'])
            api = tweepy.API(auth)

            options = self.get_api_options(self.last_search)
            statuses = tweepy.Cursor(api.user_timeline, **options).items(TWEET_COUNT)

            return sorted(statuses, key=lambda s: s.text, reverse=True)

        except Exception:
            self.log(traceback.format_exc())


    def get_api_options(self, last_search):
        '''Twitter APIで使うオプションの内容を取得'''
        if last_search:
            return {
                'id': os.environ['USER_ID'],
                'since_id': last_search.prev_since_id
            }
        else:
            return {'id': os.environ['USER_ID']}


    def save_with_transaction(self, statuses):
        '''トランザクションで各種テーブルを更新する'''
        try:
            with transaction.atomic():
                # リンゴ情報を含むツイートのみを保存
                ringo_tweets = self.delete_unrelated_tweets(statuses)
                if ringo_tweets:
                    # この方法だとcreated_at順ではなく品種順になるけど、
                    # DB上特に困ることはないので、このままで良い
                    for c in self.cultivars:
                        # 条件を満たすリストの要素に対して処理を行うために内包表記を使ってるけど
                        # 内包表記をこのように使って良いのかは分からない...
                        # バッククォート(`)で囲まれた部分を品種とみなす
                        [self.save_tweets(t, c) for t in ringo_tweets if "`" + c['Name'] + "`" in t.text]

                # 検索済idの保存
                self.save_last_search(self.last_search, statuses[0].id)

            print('commit')

        # 例外が発生した場合は、Djangoが自動的にロールバックする
        except Exception:
            self.log(traceback.format_exc())
            print('rollback')


    def delete_unrelated_tweets(self, statuses):
        '''ツイートのうち、[リンゴ]で始まるもの以外を削除'''
        pattern = re.compile('\[リンゴ\]')
        return [x for x in statuses if pattern.match(x.text)]


    def save_tweets(self, twitter_status, cultivar):
        '''ツイートの保存'''
        arg = {
            'name': cultivar['Name'],
            'tweet_id': twitter_status.id,
            'tweet': twitter_status.text,
            'tweeted_at': LOCAL_TIMEZONE.localize(twitter_status.created_at)
        }
        t = Tweets(**arg)
        t.save()


    def save_last_search(self, last_searched, prev_since_id):
        '''検索済のうち、最新のIDを保存'''
        if last_searched:
            last_searched.prev_since_id = prev_since_id
            last_searched.save()
        else:
            arg = {
                'prev_since_id': prev_since_id
            }
            l = LastSearch(**arg)
            l.save()


    def log(self, log_message):
        '''ログを出力し、設定されていればSlackへも通知する'''
        print(log_message)

        if os.environ['SLACK_TOKEN']:
            slack = Slacker(os.environ['SLACK_TOKEN'])
            slack.chat.post_message(os.environ['SLACK_CHANNEL'], log_message)
