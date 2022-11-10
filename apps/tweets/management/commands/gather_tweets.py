import os
import re
import traceback
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction
from slacker import Slacker
from tweepy import Client
from google.cloud import secretmanager
import json

from apps.cultivar.apple import Apple
from apps.tweets.models import Tweets, LastSearch
from django.conf import settings


class Command(BaseCommand):
    # 最大 pagination 回数。デフォルトで100件さがすので、100 * 40 = 4,000/日 のツイートしなければ大丈夫
    MAX_PAGINATION = 40

    def handle(self, *args, **options):
        """ manage.pyで使うときのエントリポイント """
        self.twitter_client = self.get_twitter_client()
        self.cultivars = Apple().cultivars
        self.last_search = self.get_last_search()

        print('start =====>')
        tweets, newest_id = self.fetch_tweets()
        print(tweets)
        if tweets and newest_id:
            self.save_with_transaction(tweets, newest_id)

        print('<===== finish')

    def get_last_search(self) -> LastSearch:
        """ 前回検索情報を取得する """
        return LastSearch.objects.first()

    def get_twitter_client(self):
        twitter_tokens = self.fetch_secret_manager()

        return Client(
            consumer_key=twitter_tokens['twitter_consumer_key'],
            consumer_secret=twitter_tokens['twitter_consumer_secret'],
            access_token=twitter_tokens['twitter_access_token'],
            access_token_secret=twitter_tokens['twitter_access_token_secret']
        )

    def fetch_secret_manager(self):
        if settings.DEBUG:
            client = secretmanager.SecretManagerServiceClient.from_service_account_json('gcp_credential.json')
        else:
            # Cloud Run上であれば、認証情報は取得できている
            client = secretmanager.SecretManagerServiceClient()

        path = client.secret_version_path(os.environ['GCP_PROJECT_ID'], 'twitter_tokens', 'latest')
        response = client.access_secret_version(name=path)
        value = response.payload.data.decode('UTF-8')

        # strからdictにする
        return json.loads(value)

    def fetch_tweets(self):
        """ ツイートを取得する

            戻り値
            tweets 取得したTweetオブジェクト
            newest_id 検索した最新のツイートID
        """
        tweets = []
        newest_id = 0
        pagination_token = None
        counter = 0  # 無限ループにならないよう制御

        while True:
            counter += 1

            # データがあり、かつ、ページ分割されている場合
            # => Response(data=[<Tweet id=*** text='***'>, ...], includes={}, errors=[],
            #    meta={'result_count': 5, 'newest_id': '***', 'oldest_id': '***', 'next_token': '***'})
            # データはあるが、ページ分割されていない場合、metaにnext_tokenがない
            # => Response(data=[<Tweet id=*** text='***'>, ...], includes={}, errors=[],
            #    meta={'result_count': 1, 'newest_id': '***', 'oldest_id': '***'})
            response = self.fetch_tweets_from_api(pagination_token=pagination_token)

            # self.last_search.prev_since_id が最新の場合、レスポンスは以下になる
            # Response(data=None, includes={}, errors=[], meta={'result_count': 0})
            if not response.data:
                break

            tweets += response.data

            # 最新の newest_id のみ保持しておく
            if not newest_id:
                newest_id = response.meta.get('newest_id')

            pagination_token = response.meta.get('next_token')
            if counter >= self.MAX_PAGINATION or not pagination_token:
                break

        return tweets, newest_id

    def fetch_tweets_from_api(self, pagination_token):
        return self.twitter_client.get_users_tweets(
            id=os.environ['TWITTER_USER_ID'],
            exclude=['retweets', ],
            tweet_fields=['created_at', ],
            since_id=self.last_search.prev_since_id,
            user_auth=True,
            pagination_token=pagination_token
        )

    def save_with_transaction(self, tweets: List, newest_id):
        """ トランザクションで各種テーブルを更新する """
        try:
            with transaction.atomic():
                # リンゴ情報を含むツイートのみを保存
                ringo_tweets = self.delete_unrelated_tweets(tweets)

                if ringo_tweets:
                    # この方法だとcreated_at順ではなく品種順になるけど、
                    # DB上特に困ることはないので、このままで良い
                    for c in self.cultivars:
                        # 条件を満たすリストの要素に対して処理を行うために内包表記を使ってる
                        # バッククォート(`)で囲まれた部分を品種とみなす
                        [self.save_tweets(tweet, c) for tweet in ringo_tweets if "`" + c['Name'] + "`" in tweet.text]

                # 検索済idの保存
                self.save_last_search(self.last_search, newest_id)

            print('commit')

        # 例外が発生した場合は、Djangoが自動的にロールバックする
        except Exception as e:
            self.log(traceback.format_exc())
            print('rollback')

    def delete_unrelated_tweets(self, tweets: List) -> List:
        """ ツイートのうち、[リンゴ]で始まるもの以外を削除 """
        pattern = re.compile(r'\[リンゴ\]')
        return [tweet for tweet in tweets if pattern.match(tweet.text)]

    def save_tweets(self, tweet, cultivar: dict):
        """ ツイートの保存 """

        # tweet_idがユニークキーになっているため、念のためget_or_createする
        Tweets.objects.get_or_create(
            name=cultivar['Name'],
            tweet_id=tweet.id,
            tweet=tweet.text,
            tweeted_at=tweet.created_at
        )

    def save_last_search(self, last_searched: LastSearch, newest_id: int):
        """ 検索済のうち、最新のIDを保存 """

        current_since_id = last_searched.prev_since_id if last_searched else -1

        LastSearch.objects.update_or_create(
            prev_since_id=current_since_id,
            defaults={
                'prev_since_id': newest_id
            }
        )

    def log(self, log_message: str):
        """ ログを出力し、設定されていればSlackへも通知する """
        print(log_message)

        if os.environ.get('SLACK_TOKEN'):
            slack = Slacker(os.environ['SLACK_TOKEN'])
            slack.chat.post_message(os.environ['SLACK_CHANNEL'], log_message)
