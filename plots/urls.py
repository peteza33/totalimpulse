from django.conf.urls import include, url

from plots import views

urlpatterns = [
    url(r'^sc-drag-comp/', views.sc_drag, name = 'plots_sc_drag'),

    url(r'^DV-drop-SSO/', views.delta_v, name = 'plots_delta_v'),

    url(r'^thruster-performance/', views.thruster_performance, name = 'plots_thruster_performance'),

    url(r'^EP-prop-dutycycle/', views.ep_prop_dutycycle, name = 'plots_ep_prop_dutycycle'),
]