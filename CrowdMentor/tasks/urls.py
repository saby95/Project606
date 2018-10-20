from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<task_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^claimed/$', views.claimed_tasks, name='claimed_tasks'),
    url(r'^(?P<task_id>[0-9]+)/claim$', views.claim, name='claim'),
]