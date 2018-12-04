from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<ques_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<ques_id>[0-9]+)/upvote$', views.ques_upvote, name='ques_upvote'),
    url(r'^(?P<ques_id>[0-9]+)/(?P<ans_id>[0-9]+)/upvote$', views.ans_upvote, name='ans_upvote'),
    url(r'^(?P<ques_id>[0-9]+)/downvote$', views.ques_downvote, name='ques_downvote'),
    url(r'^(?P<ques_id>[0-9]+)/(?P<ans_id>[0-9]+)/downvote$', views.ans_downvote, name='ans_downvote'),
    url(r'^add_ques/$', views.add_question, name='add_question'),
]