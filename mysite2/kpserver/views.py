#coding:utf-8
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from .retrace_data import *


# Create your views here.

@csrf_exempt
def index(request):
    result = Request(request)
    return HttpResponse(result)
