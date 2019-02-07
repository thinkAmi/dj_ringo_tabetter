from collections import namedtuple
from datetime import datetime

import pytest

from apps.tweets.tests.factories import LastSearchFactory

Status = namedtuple('Status', ('id', 'text', 'created_at'))


@pytest.fixture
def cultivars():
    return [
        {'Name': 'シナノゴールド', 'Color': 'Gold'},
        {'Name': 'シナノドルチェ', 'Color': 'Red'},
        {'Name': '王林', 'Color': 'Yellow'},
    ]


@pytest.mark.freeze_time("2019-01-01")
@pytest.mark.django_db(transaction=True)
class TestGatherTweets:
    def test_get_last_search(self):
        from apps.tweets.management.commands.gather_tweets import Command

        last_search = LastSearchFactory()

        command = Command()
        actual = command.get_last_search()
        assert last_search.prev_since_id == actual.prev_since_id

    def test_gather_tweet(self):
        from apps.tweets.management.commands.gather_tweets import Command

        statuses = [
            Status(id=3, text='あいうえお', created_at=datetime.now()),
            Status(id=2, text='さしすせそ', created_at=datetime.now()),
            Status(id=1, text='かきくけこ', created_at=datetime.now()),
        ]

        command = Command()
        command._get_statuses_from_api = lambda: statuses

        actual = command.gather_tweets()
        assert actual == [
            Status(id=2, text='さしすせそ', created_at=datetime.now()),
            Status(id=1, text='かきくけこ', created_at=datetime.now()),
            Status(id=3, text='あいうえお', created_at=datetime.now()),
        ]

    def test_get_api_options_last_searchがない場合(self, monkeypatch):
        from apps.tweets.management.commands.gather_tweets import Command

        env_value = 'foo'
        monkeypatch.setenv('USER_ID', env_value)

        command = Command()
        actual = command.get_api_options(None)

        assert actual == {'id': env_value}

    def test_get_api_options_last_searchがある場合(self, monkeypatch):
        from apps.tweets.management.commands.gather_tweets import Command

        env_value = 'foo'
        monkeypatch.setenv('USER_ID', env_value)

        last_search = LastSearchFactory(prev_since_id=200)
        command = Command()
        actual = command.get_api_options(last_search)

        assert actual == {
            'id': env_value,
            'since_id': last_search.prev_since_id,
        }

    def test_save_with_transaction_該当ツイート無し_LastSearch無しの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        command = Command()
        command.cultivars = cultivars
        command.last_search = None

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='リンゴ 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日はシナノゴールドを食べた', created_at=datetime.now()),
            Status(id=1, text='[りんご] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
        ]
        command.save_with_transaction(statuses)

        assert Tweets.objects.count() == 0

        after_last_search = LastSearch.objects.all()
        assert len(after_last_search) == 1
        assert after_last_search.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイート無し_LastSearchありの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        command = Command()
        command.cultivars = cultivars
        command.last_search = LastSearchFactory()

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='リンゴ 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日はシナノゴールドを食べた', created_at=datetime.now()),
            Status(id=1, text='[りんご] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
        ]
        command.save_with_transaction(statuses)

        assert Tweets.objects.count() == 0

        after_last_search = LastSearch.objects.all()
        assert len(after_last_search) == 1
        assert after_last_search.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイートあり_LastSearch無しの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        command = Command()
        command.cultivars = cultivars
        command.last_search = None

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='[リンゴ] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日は`シナノドルチェ`を食べた', created_at=datetime.now()),
            Status(id=1, text='[リンゴ] 今日は `王林` を食べた', created_at=datetime.now()),
        ]
        command.save_with_transaction(statuses)

        assert Tweets.objects.count() == 3
        assert Tweets.objects.filter(name='シナノゴールド').count() == 1
        assert Tweets.objects.filter(name='シナノドルチェ').count() == 1
        assert Tweets.objects.filter(name='王林').count() == 1

        last_search = LastSearch.objects.all()
        assert len(last_search) == 1
        assert last_search.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイートあり_LastSearchありの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        command = Command()
        command.cultivars = cultivars
        command.last_search = LastSearchFactory()

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='[リンゴ] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日は`シナノドルチェ`を食べた', created_at=datetime.now()),
            Status(id=1, text='[リンゴ] 今日は `王林` を食べた', created_at=datetime.now()),
        ]
        command.save_with_transaction(statuses)

        assert Tweets.objects.count() == 3
        assert Tweets.objects.filter(name='シナノゴールド').count() == 1
        assert Tweets.objects.filter(name='シナノドルチェ').count() == 1
        assert Tweets.objects.filter(name='王林').count() == 1

        last_search = LastSearch.objects.all()
        assert len(last_search) == 1
        assert last_search.first().prev_since_id == 3
