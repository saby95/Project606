# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import BroadcastMessages

@login_required
def index(request):
    user = User.objects.get(username=request.user.username)
    role = user.profile.role
    broadcast_messages = BroadcastMessages.objects.filter(group_role=role, claim=False)

    context = {
        'broadcast_messages': broadcast_messages,
    }
    return render(request, 'broadcast/index.html', context)

@login_required
def claim_broadcast(request):
    broadcast_id = request.POST.get("broadcast_id")
    broadcast = get_object_or_404(BroadcastMessages, id=broadcast_id)
    broadcast.claim = True
    broadcast.claim_by = request.user
    broadcast.save()

    return redirect('messages_view')