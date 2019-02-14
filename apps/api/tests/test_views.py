""" とりあえず正常系のテストだけ：異常系は起こらないはず... """

from datetime import datetime

import pytest
import pytz

from apps.tweets.tests.factories import TweetsFactory


@pytest.fixture
def total_apples_expected():
    for i in range(3):
        TweetsFactory(name='フジ')
    for i in range(2):
        TweetsFactory(name='シナノドルチェ')
    for i in range(5):
        TweetsFactory(name='シナノゴールド')

    return '''[
  {
    "name": "シナノドルチェ",
    "y": 2,
    "color": "AntiqueWhite"
  },
  {
    "name": "シナノゴールド",
    "y": 5,
    "color": "Gold"
  },
  {
    "name": "フジ",
    "y": 3,
    "color": "Red"
  }
]'''


@pytest.mark.django_db(transaction=True)
class TestTotalApples:
    """ total_apples() のテスト """

    def test_get(self, client, total_apples_expected):
        actual = client.get('/api/v1/total/')
        assert actual.content.decode('utf-8') == total_apples_expected


@pytest.fixture
def total_apples_by_month_expected():
    for i in range(1, 4):
        # RuntimeWarningを避けるため、tzinfoを渡す
        # RuntimeWarning:
        # DateTimeField Tweets.tweeted_at received a naive datetime (2019-01-10 00:00:00)
        # while time zone support is active.
        TweetsFactory(name='フジ',
                      tweeted_at=datetime(2019, i, 10, tzinfo=pytz.timezone("Asia/Tokyo")))
    for i in range(1, 3):
        TweetsFactory(name='シナノドルチェ',
                      tweeted_at=datetime(2019, i, 10, tzinfo=pytz.timezone("Asia/Tokyo")))
    for i in range(1, 6):
        TweetsFactory(name='シナノゴールド',
                      tweeted_at=datetime(2019, i, 10, tzinfo=pytz.timezone("Asia/Tokyo")))

    return '''[
  {
    "name": "フジ",
    "data": [
      1,
      1,
      1,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "color": "Red"
  },
  {
    "name": "シナノゴールド",
    "data": [
      1,
      1,
      1,
      1,
      1,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "color": "Gold"
  },
  {
    "name": "シナノドルチェ",
    "data": [
      1,
      1,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "color": "AntiqueWhite"
  }
]'''


@pytest.mark.django_db(transaction=True)
class TestTotalApplesByMonth:
    """ total_apples_by_month()のテスト """

    def test_get(self, client, total_apples_by_month_expected):
        actual = client.get('/api/v1/month/')
        assert actual.content.decode('utf-8') == total_apples_by_month_expected
