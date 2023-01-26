from django.shortcuts import render
from django.http import HttpResponse
from DS_CORE.diggy_spidy import *
def help(request):
    ds_obj.scrap('https://example.com')
    return HttpResponse("Help")

def scrape(request):
    return HttpResponse("")