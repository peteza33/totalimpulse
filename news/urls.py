from django.conf.urls import include, url

from news import views

urlpatterns = [
    url(r'^$', views.latest_news, name = 'latest_news'),
]