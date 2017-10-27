from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^addpage$', views.addpage),
    url(r'^create$', views.create),
    url(r'^main/display/(?P<item_id>\d+)$', views.display),
    url(r'^add/(?P<item_id>\d+)$', views.add),
    url(r'^remove/(?P<item_id>\d+)$', views.remove),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
