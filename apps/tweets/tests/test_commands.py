from collections import namedtuple
from datetime import datetime

import pytest
from django.core.management import call_command
from unittest.mock import Mock, patch

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

        sut = Command()
        actual = sut.get_last_search()
        assert actual.prev_since_id == last_search.prev_since_id

    def test_gather_tweet(self):
        from apps.tweets.management.commands.gather_tweets import Command

        statuses = [
            Status(id=3, text='あいうえお', created_at=datetime.now()),
            Status(id=2, text='さしすせそ', created_at=datetime.now()),
            Status(id=1, text='かきくけこ', created_at=datetime.now()),
        ]

        sut = Command()
        sut._get_statuses_from_api = lambda: statuses  # 内部で呼ばれるメソッドを差し替え

        actual = sut.gather_tweets()
        assert actual == statuses

    def test_get_api_options_last_searchがない場合(self, monkeypatch):
        from apps.tweets.management.commands.gather_tweets import Command

        env_value = 'foo'
        monkeypatch.setenv('USER_ID', env_value)

        sut = Command()
        actual = sut.get_api_options(None)

        assert actual == {'id': env_value}

    def test_get_api_options_last_searchがある場合(self, monkeypatch):
        from apps.tweets.management.commands.gather_tweets import Command

        env_value = 'foo'
        monkeypatch.setenv('USER_ID', env_value)

        last_search = LastSearchFactory(prev_since_id=200)
        sut = Command()
        actual = sut.get_api_options(last_search)

        assert actual == {
            'id': env_value,
            'since_id': last_search.prev_since_id,
        }

    def test_save_with_transaction_該当ツイート無し_LastSearch無しの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        sut = Command()
        sut.cultivars = cultivars
        sut.last_search = None

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='リンゴ 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日はシナノゴールドを食べた', created_at=datetime.now()),
            Status(id=1, text='[りんご] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
        ]
        sut.save_with_transaction(statuses)

        assert Tweets.objects.count() == 0

        actual = LastSearch.objects.all()
        assert len(actual) == 1
        assert actual.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイート無し_LastSearchありの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        sut = Command()
        sut.cultivars = cultivars
        sut.last_search = LastSearchFactory()

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='リンゴ 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日はシナノゴールドを食べた', created_at=datetime.now()),
            Status(id=1, text='[りんご] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
        ]
        sut.save_with_transaction(statuses)

        assert Tweets.objects.count() == 0

        actual = LastSearch.objects.all()
        assert len(actual) == 1
        assert actual.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイートあり_LastSearch無しの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        sut = Command()
        sut.cultivars = cultivars
        sut.last_search = None

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='[リンゴ] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日は`シナノドルチェ`を食べた', created_at=datetime.now()),
            Status(id=1, text='[リンゴ] 今日は `王林` を食べた', created_at=datetime.now()),
        ]
        sut.save_with_transaction(statuses)

        assert Tweets.objects.count() == 3
        assert Tweets.objects.filter(name='シナノゴールド').count() == 1
        assert Tweets.objects.filter(name='シナノドルチェ').count() == 1
        assert Tweets.objects.filter(name='王林').count() == 1

        actual = LastSearch.objects.all()
        assert len(actual) == 1
        assert actual.first().prev_since_id == 3

    def test_save_with_transaction_該当ツイートあり_LastSearchありの場合(self, cultivars):
        from apps.tweets.management.commands.gather_tweets import Command
        from apps.tweets.models import Tweets, LastSearch

        sut = Command()
        sut.cultivars = cultivars
        sut.last_search = LastSearchFactory()

        # Twitterの仕様では、新しいものから順に取得できる(添字が小さいほど、最近の投稿になる)
        statuses = [
            Status(id=3, text='[リンゴ] 今日は `シナノゴールド` を食べた', created_at=datetime.now()),
            Status(id=2, text='[リンゴ] 今日は`シナノドルチェ`を食べた', created_at=datetime.now()),
            Status(id=1, text='[リンゴ] 今日は `王林` を食べた', created_at=datetime.now()),
        ]
        sut.save_with_transaction(statuses)

        assert Tweets.objects.count() == 3
        assert Tweets.objects.filter(name='シナノゴールド').count() == 1
        assert Tweets.objects.filter(name='シナノドルチェ').count() == 1
        assert Tweets.objects.filter(name='王林').count() == 1

        actual = LastSearch.objects.all()
        assert len(actual) == 1
        assert actual.first().prev_since_id == 3

    def test_call_command_Djangoコマンドを直接呼ぶ(self):
        from apps.tweets.management.commands import gather_tweets

        with patch.object(
                gather_tweets, 'Apple', return_value=Mock()) as apple, \
            patch.object(
                gather_tweets.Command, 'get_last_search') as mock_get, \
            patch.object(
                gather_tweets.Command, 'gather_tweets', return_value='foo') as mock_gather, \
            patch.object(
                gather_tweets.Command, 'save_with_transaction') as mock_save:

            # 作成したDjangoコマンドを直接呼ぶ
            call_command('gather_tweets')

            # コマンドの内部で呼ばれるはずのメソッドが、想定通り呼ばれているかをチェック
            mock_get.assert_called_with()
            mock_gather.assert_called_with()
            mock_save.assert_called_with('foo')  # mockで foo を返しているので、それが使われるか
