from collections import namedtuple
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from tweepy import Response

from apps.tweets.tests.factories import LastSearchFactory

Tweet = namedtuple('Tweet', ('id', 'text', 'created_at'))


@pytest.fixture
def cultivars():
    return [
        {'Name': 'シナノゴールド', 'Color': 'Gold'},
        {'Name': 'シナノドルチェ', 'Color': 'Red'},
        {'Name': '王林', 'Color': 'Yellow'},
    ]


@pytest.fixture()
def twitter_response():
    return Response(
            data=[
                Tweet(id=3, text='[リンゴ] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
                Tweet(id=2, text='[リンゴ] 今日は`シナノドルチェ`を食べた', created_at=datetime.now()),
                Tweet(id=1, text='[リンゴ] 今日は `王林` を食べた', created_at=datetime.now()),
            ],
            meta={'result_count': 3, 'newest_id': '3', 'oldest_id': '1', 'next_token': 'abc'},
            includes=[],
            errors=[],
        )


@pytest.mark.freeze_time("2019-01-01")
@pytest.mark.django_db(transaction=True)
class TestGatherTweets:
    def test_get_last_search(self):
        from apps.tweets.management.commands.gather_tweets import Command

        last_search = LastSearchFactory()

        sut = Command()
        actual = sut.get_last_search()
        assert actual.prev_since_id == last_search.prev_since_id

    def test_gather_tweet(self, twitter_response):
        from apps.tweets.management.commands.gather_tweets import Command

        sut = Command()

        # メソッドや定数を差し替え
        sut.MAX_PAGINATION = 1
        sut.get_twitter_client = lambda: None
        sut.fetch_tweets_from_api = lambda pagination_token: twitter_response

        tweets, newest_id = sut.fetch_tweets()
        assert tweets == twitter_response.data
        assert newest_id == '3'

    def test_save_with_transaction_LastSearch無しの場合(self, cultivars, twitter_response):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        sut = Command()
        sut.cultivars = cultivars
        sut.last_search = None

        sut.save_with_transaction(twitter_response.data, newest_id='3')

        assert Tweets.objects.count() == 3
        assert Tweets.objects.filter(name='シナノゴールド').count() == 1
        assert Tweets.objects.filter(name='シナノドルチェ').count() == 1
        assert Tweets.objects.filter(name='王林').count() == 1

        actual = LastSearch.objects.all()
        assert len(actual) == 1
        assert actual.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイートあり_LastSearchありの場合(self, cultivars, twitter_response):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        sut = Command()
        sut.cultivars = cultivars
        sut.last_search = LastSearchFactory()

        sut.save_with_transaction(twitter_response.data, newest_id='3')

        assert Tweets.objects.count() == 3
        assert Tweets.objects.filter(name='シナノゴールド').count() == 1
        assert Tweets.objects.filter(name='シナノドルチェ').count() == 1
        assert Tweets.objects.filter(name='王林').count() == 1

        actual = LastSearch.objects.all()
        assert len(actual) == 1
        assert actual.first().prev_since_id == 3

    def test_call_command_Djangoコマンドを直接呼ぶ(self, twitter_response):
        from apps.tweets.management.commands import gather_tweets

        with patch.object(
                gather_tweets, 'Apple', return_value=Mock()) as apple, \
            patch.object(
                gather_tweets.Command, 'get_last_search') as mock_get, \
            patch.object(
                gather_tweets.Command, 'fetch_tweets', return_value=[twitter_response, '3']) as mock_gather, \
            patch.object(
                gather_tweets.Command, 'save_with_transaction') as mock_save:

            # 作成したDjangoコマンドを直接呼ぶ
            call_command('gather_tweets')

            # コマンドの内部で呼ばれるはずのメソッドが、想定通り呼ばれているかをチェック
            mock_get.assert_called_with()
            mock_gather.assert_called_with()
            mock_save.assert_called_with(twitter_response, '3')  # mockで foo を返しているので、それが使われるか
