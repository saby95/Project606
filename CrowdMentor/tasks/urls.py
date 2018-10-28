from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_tasks/$', views.add_tasks, name='add_tasks'),
    url(r'^(?P<task_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^claimed/$', views.claimed_tasks, name='claimed_tasks'),
    url(r'^(?P<task_id>[0-9]+)/claim$', views.claim, name='claim'),
    url(r'^claimed/(?P<task_id>[0-9]+)/answer$', views.answer, name='answer'),
    url(r'^audits/$', views.audit_tasks, name='audit_tasks'),
    url(r'^open_audits/$', views.open_audits, name='open_audits'),
    url(r'^audits/(?P<task_id>[0-9]+)/claim_audit', views.claim_audit, name='claim_audit'),
    url(r'^audits/(?P<task_id>[0-9]+)/submit_audit', views.submit_audit, name='submit_audit'),
    url(r'^open_audits/(?P<task_id>[0-9]+)/$', views.detail_audit, name='detail_audit'),
]