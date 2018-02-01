from django.conf.urls import include, url

from news import views

urlpatterns = [
    url(r'^prop', views.prop_news, name = 'prop_news'),

    url(r'^smallsat', views.sat_news, name = 'sat_news'),
]