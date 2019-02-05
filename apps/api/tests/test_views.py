""" とりあえず正常系のテストだけ：異常系は起こらないはず... """

from collections import OrderedDict
from datetime import datetime

import pytest
import pytz
from django.test.client import RequestFactory

from apps.api.tests.factories import TweetsFactory


class TestRenderJsonResponse:
    """ render_json_response()のテスト """

    def test_直接呼ぶ(self):
        from apps.api.views import render_json_response

        request = RequestFactory()

        # dumpした時の順番を一定にするため、OrderedDictを使う
        data = OrderedDict([
            ('foo', 'シナノゴールド'),
            ('bar', ['ham', 'ハム']),
        ])

        expected = '''{
  "foo": "シナノゴールド",
  "bar": [
    "ham",
    "ハム"
  ]
}'''

        actual = render_json_response(request, data)
        assert actual.content.decode('utf-8') == expected


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
    "quantity": 2,
    "color": "AntiqueWhite"
  },
  {
    "name": "シナノゴールド",
    "quantity": 5,
    "color": "Gold"
  },
  {
    "name": "フジ",
    "quantity": 3,
    "color": "Red"
  }
]'''


@pytest.mark.django_db(transaction=True)
class TestTotalApples:
    """ total_apples() のテスト """

    def test_直接呼ぶ(self, total_apples_expected):
        from apps.api.views import total_apples

        request = RequestFactory()
        actual = total_apples(request)

        assert actual.content.decode('utf-8') == total_apples_expected

    def test_Client経由で呼ぶ(self, client, total_apples_expected):
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
    "quantity": [
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
    "quantity": [
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
    "quantity": [
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

    def test_直接呼ぶ(self, total_apples_by_month_expected):
        from apps.api.views import total_apples_by_month

        request = RequestFactory()
        actual = total_apples_by_month(request)

        assert actual.content.decode('utf-8') == total_apples_by_month_expected

    def test_Client経由で呼ぶ(self, client, total_apples_by_month_expected):
        actual = client.get('/api/v1/month/')
        assert actual.content.decode('utf-8') == total_apples_by_month_expected
