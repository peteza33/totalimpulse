from django.conf.urls import include, url

from news import views

urlpatterns = [
    url(r'^$', views.links, name = 'news_links'),
]