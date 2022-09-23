import os

from django.core.management.base import BaseCommand
from tweepy import Client


class Command(BaseCommand):
    """ Twitter GET /2/users/me から自分の user_id を取得し、コンソールに表示する

        https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_me
        なお、取得した user_id は .env や環境変数に設定すること
    """
    def handle(self, *args, **options):
        client = Client(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        )

        response = client.get_me()
        print(response)
