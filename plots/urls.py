from django.conf.urls import include, url

from plots import views

urlpatterns = [
    url(r'^$', views.plots_home, name = "plots_home"),

    url(r'^line/', views.plots_line, name = 'plots_line'),
]