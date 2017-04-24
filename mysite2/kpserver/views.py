#coding:utf-8
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from .retrace_data import *
from configure import *
import json
import sys

# Create your views here.

@csrf_exempt
def index(request):
    if request.method == "POST":
        result = Request(request)
        return HttpResponse(result)
    else:
        result = Request(request)
        return HttpResponse(result)