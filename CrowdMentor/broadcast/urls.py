from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^claim$', views.claim_broadcast, name='claim_broadcast'),
    ]