from django.http import HttpResponse
from django.db import models
import json
from collections import OrderedDict
from apps.tweets.models import Tweets
from libs.cultivars import Apple

def render_json_response(request, data, status=None):
    '''responseをJSONで返す'''
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    response = HttpResponse(json_str, content_type='application/json; charset=utf-8', status=status)
    return response


def total_apples(request):
    '''リンゴの品種別合計数量を返す'''
    results = []
    apples = Apple()

    # valuesで取得したい項目、annotateで別途集計したい項目をそれぞれ取得できる
    for tweet in Tweets.objects.values('name').annotate(quantity=models.Count('name')):

        apple_dict = OrderedDict([
            ('name', tweet['name']),
            ('quantity', tweet['quantity']),
            ('color', apples.get_color(tweet['name']))
        ])
        results.append(apple_dict)

    return render_json_response(request, results)


def total_apples_by_month(request):
    '''リンゴの月別品種別合計数量を返す'''
    results = []
    apples = Apple()
    tweets = Tweets.objects.extra(select={ 'month': "date_part('month', tweeted_at)::int" }) \
        .values('name', 'month').annotate(quantity=models.Count('name')).order_by('name', 'month')

    # DBで縦持ちしているものをHighchartsのために横持ちにする
    name = tweets[0]['name']
    quantities = [0] * 12

    for tweet in tweets:
        if name != tweet['name']:
            results.append(OrderedDict([
                ('name', name),
                ('quantity', quantities),
                ('color', apples.get_color(name))
            ]))

            name = tweet['name']
            quantities = [0] * 12

        quantities[tweet['month'] - 1] = tweet['quantity']

    results.append(OrderedDict([
        ('name', name),
        ('quantity', quantities),
        ('color', apples.get_color(name))
    ]))
    return render_json_response(request, results)
