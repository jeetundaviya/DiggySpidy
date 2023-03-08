from django.shortcuts import render
from django.http import HttpResponse
from DS_CORE.diggy_spidy import *
def help(request):
    # ds_obj.is_slow_mode = True
    ds_obj.crawl('https://example.com')
    return HttpResponse("Help")

def scrape(request):
    return HttpResponse("")