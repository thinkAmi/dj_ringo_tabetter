from django.shortcuts import render


def total(request):
    """ 品種別の合計数量 """
    return render(request, 'highcharts/total.jinja2')


def total_by_month(request):
    """ 月別品種別の合計数量 """
    return render(request, 'highcharts/total_by_month.jinja2')
