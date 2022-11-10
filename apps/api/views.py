import os

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.cultivar.apple import Apple
from apps.tweets.models import Tweets

from google.auth.transport import requests
from google.oauth2 import id_token
from django.core.management import call_command


class RingoJsonResponse(JsonResponse):
    """ ringo-tabetter用設定を行ったJsonResponseオブジェクト(薄いラッパー) """

    def __init__(self, data):
        """

        :param data: JSON化するデータ
        """
        super().__init__(data=data,
                         safe=False,
                         json_dumps_params={'ensure_ascii': False, 'indent': 2})


# -------------
# Highcharts用
# -------------

class TotalApplesView(View):
    """ リンゴの品種別合計数量を返すView """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> RingoJsonResponse:
        results = []
        apples = Apple()

        for tweet in Tweets.calculate_total_by_name().all():
            apple_dict = dict(
                name=tweet['name'],
                y=tweet['quantity'],
                color=apples.get_color(tweet['name']),
            )
            results.append(apple_dict)
        return RingoJsonResponse(results)


class TotalApplesByMonthView(View):
    """ リンゴの月別品種別合計数量を返すView """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> RingoJsonResponse:
        results = []
        apples = Apple()
        tweets = Tweets.calculate_total_by_name_and_month()

        # DBで縦持ちしているものをHighchartsのために横持ちにする
        name = tweets[0]['name']
        quantities = [0] * 12

        for tweet in tweets:
            if name != tweet['name']:
                results.append({
                    'name': name,
                    'data':  quantities,
                    'color': apples.get_color(name),
                })

                name = tweet['name']
                quantities = [0] * 12

            # SQLiteの場合、日付は文字列での表現なため、int()で数値に変換する
            quantities[int(tweet['month']) - 1] = tweet['quantity']

        results.append({
            'name': name,
            'data':  quantities,
            'color': apples.get_color(name),
        })
        return RingoJsonResponse(results)


class GatherTweetView(View):
    """ Cloud Schedulerからのリクエストを受け付ける View """

    http_method_names = ['get']
    client_id = os.environ['SCHEDULER_CLIENT_ID']

    def get(self, request, *args, **kwargs) -> RingoJsonResponse:
        authz_header = request.headers.get('Authorization')
        received_id_token = authz_header.replace('Bearer', '').lstrip()

        try:
            # 認証
            id_token.verify_oauth2_token(received_id_token, requests.Request(), self.client_id)

            # tweetの収集
            call_command('gather_tweets')

            return RingoJsonResponse({
                'status': 'success'
            })
        except ValueError as e:
            print(e)
            return RingoJsonResponse({
                'status': 'unauthorized'
            })
