from django.conf.urls import include, url

from plots import views

urlpatterns = [
    url(r'^line/', views.line, name = "line"),
]