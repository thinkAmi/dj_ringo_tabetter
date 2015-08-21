from django.shortcuts import render_to_response

def total(request):
    '''品種別の合計数量'''
    return render_to_response('total.jinja2')


def total_by_month(request):
    '''月別品種別の合計数量'''
    return render_to_response('total_by_month.jinja2')
