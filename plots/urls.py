from django.conf.urls import include, url

from plots import views

urlpatterns = [
    url(r'^simple_chart/$', views.simple_chart, name="simple_chart"),
]