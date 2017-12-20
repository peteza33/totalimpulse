from django.conf.urls import include, url

from plots import views

urlpatterns = [
    url(r'^sc-drag-comp/', views.sc_life, name = 'plots_sc_drag'),

    url(r'^DV-drop-SSO/', views.delta_v, name = 'plots_delta_v'),
]