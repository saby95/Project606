from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

from .models import ResearchTasks

@login_required
def index(request):
    task_list = ResearchTasks.objects.filter(worker_id__isnull=True)
    context = {
        'task_list': task_list,
    }
    return render(request, 'tasks/index.html', context)

@login_required
def add_tasks(request):
    return render(request, 'tasks/add_task.html')

@login_required
def detail(request, task_id):
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except ResearchTask.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail.html', {'task': task})

@login_required
def claimed_tasks(request):
    user_id = User.objects.get(username=request.user.username).id
    task_list = ResearchTasks.objects.filter(worker_id=user_id)
    context = {
        'task_list': task_list,
    }
    return render(request, 'tasks/claimed_task.html', context)

@login_required
def claim(request, task_id):
    user = User.objects.get(username=request.user.username)
    try:
        task = ResearchTasks.objects.get(pk=task_id)
        task.worker_id = user
        task.claim_time = datetime.now()
        task.save()
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    return redirect('/tasks/')
