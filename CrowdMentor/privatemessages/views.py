# Create your views here.

import os
import redis
import urlparse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from privatemessages.models import Thread
from users.profile import Profile
from users.UserRoles import UserRoles
from privatemessages.utils import send_message
from broadcast.models import BroadcastMessages
from django.contrib.auth.decorators import login_required
from time import sleep
from django.contrib import messages

@login_required
def send_message_view(request):
    if not request.method == "POST":
        return HttpResponse("Please use POST.")

    message_text = request.POST.get("message")

    if not message_text:
        messages.warning(request, 'Message Blank')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if len(message_text) > 10000:
        messages.warning(request, 'Message Too Long')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    recipient_name = request.POST.get("recipient_name")
    recipient = User.objects.get(username=recipient_name)

    thread_queryset = Thread.objects.filter(
        participants=recipient
    ).filter(
        participants=request.user
    )

    if thread_queryset.exists():
        thread = thread_queryset[0]
    else:
        thread = Thread.objects.create()
        thread.participants.add(request.user, recipient)

    send_message(
                    thread.id,
                    request.user.id,
                    message_text,
                    request.user.username
                )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def messages_view(request):
    threads = Thread.objects.filter(
        participants=request.user
    ).order_by("-last_message")

    user_id = request.user.id
    role = request.user.profile.role
    chat_participants=[]

    if role == 'mentor':
        participants = Profile.objects.filter(mentor_id=user_id)
        for usr in participants:
            user = User.objects.get(id=usr.user_id)
            chat_participants.append([user.username, user.profile.online])

    elif role == 'worker':
        participants = Profile.objects.filter(user_id=request.user.profile.mentor_id)
        for usr in participants:
            user = User.objects.get(id=usr.user_id)
            chat_participants.append([user.username, user.profile.online])

    if not threads:
        return render(request, 'messages1/private_messages.html',
                                  {
                                      "chat_participants": chat_participants,
                                  })

    #r = redis.StrictRedis()
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    urlparse.uses_netloc.append('redis')
    url = urlparse.urlparse(redis_url)
    r = redis.StrictRedis(host=url.hostname, port=url.port, db=0, password=url.password)
    #r = redis.StrictRedis(host='spinyfin.redistogo.com', port=10695, db=0, password='35461f89f6bb20899d7616def92dbd0a')

    user_id = request.user.id
    updated_threads = []
    for thread in threads:
        thread.partner = thread.participants.exclude(id=request.user.id)
        if not thread.partner:
            continue
        else:
            thread.partner = thread.partner[0]

        thread.total_messages = r.hget(
            "".join(["thread_", str(thread.id), "_messages"]),
            "total_messages"
        )
        updated_threads.append(thread)

    return render(request, 'messages1/private_messages.html',
                              {
                                  "threads": updated_threads,
                                  "chat_participants": chat_participants,
                              })

@login_required
def chat_view(request, thread_id):
    thread = get_object_or_404(
        Thread,
        id=thread_id,
        participants__id=request.user.id
    )

    messages = thread.message_set.order_by("-datetime")[:100]

    user_id = str(request.user.id)

    #r = redis.StrictRedis()
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    urlparse.uses_netloc.append('redis')
    url = urlparse.urlparse(redis_url)
    r = redis.StrictRedis(host=url.hostname, port=url.port, db=0, password=url.password)
    #r = redis.StrictRedis(host='spinyfin.redistogo.com', port=10695, db=0, password='35461f89f6bb20899d7616def92dbd0a')

    messages_total = r.hget(
        "".join(["thread_", thread_id, "_messages"]),
        "total_messages"
    )

    messages_sent = r.hget(
        "".join(["thread_", thread_id, "_messages"]),
        "".join(["from_", user_id])
    )

    if messages_total:
        messages_total = int(messages_total)
    else:
        messages_total = 0

    if messages_sent:
        messages_sent = int(messages_sent)
    else:
        messages_sent = 0

    messages_received = messages_total-messages_sent

    partner = thread.participants.exclude(id=request.user.id)[0]

    return render(request, 'messages1/chat.html',
                              {
                                  "thread_id": thread_id,
                                  "thread_messages": messages,
                                  "messages_total": messages_total,
                                  "messages_sent": messages_sent,
                                  "messages_received": messages_received,
                                  "partner": partner,
                              })


@login_required
def live_chat(request):
    broadcast_id = request.POST.get("broadcast_id")
    thread_id = request.POST.get("thread_id")
    if not broadcast_id:
        thread = Thread.objects.create()
        thread.participants.add(request.user)
        thread_id = thread.id

        broadcast = BroadcastMessages.objects.create(broadcast_type='live-chat', group_role=UserRoles.MENTOR.value,
                                                     broadcast_message='User ' + request.user.username + ' wants to chat')
        broadcast_id = broadcast.id
    else:
        broadcast = get_object_or_404(BroadcastMessages, id=broadcast_id)
        if broadcast.claim:
            thread = get_object_or_404(Thread, id=thread_id, participants__id=request.user.id)
            claiming_user = User.objects.get(id=broadcast.claim_by.id)
            thread.participants.add(claiming_user)
            return redirect('chat_view', thread_id=thread_id)
        else:
            sleep(5)    # Wait/Sleep for sometime

    return render(request, 'messages1/live.html',
                  {
                      "thread_id": thread_id,
                      "broadcast_id": broadcast_id,
                  })