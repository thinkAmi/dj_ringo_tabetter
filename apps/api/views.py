from django.http import JsonResponse
from django.views import View

from apps.cultivar.apple import Apple
from apps.tweets.models import Tweets


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

            quantities[tweet['month'] - 1] = tweet['quantity']

        results.append({
            'name': name,
            'data':  quantities,
            'color': apples.get_color(name),
        })
        return RingoJsonResponse(results)
