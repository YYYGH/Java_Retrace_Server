from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    #url(r'^admin/', admin.site.urls),
]