from django.conf.urls import url
from privatemessages import views

urlpatterns = [
    url(r'^send_message/$', views.send_message_view, name='send_message_view'),
    url(r'^chat/(?P<thread_id>\d+)/$', views.chat_view, name='chat_view'),
    url(r'^$', views.messages_view, name=''),
]
