from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

from .models import ResearchTasks, TaskUserJunction
from .forms import AddTaskForm, AnswerForm

#Controller for View Open tasks
@login_required
def index(request):
    task_list = ResearchTasks.objects.all().exclude(num_workers = 0)
    context = {
        'task_list': task_list,
    }
    return render(request, 'tasks/index.html', context)

#Controller for adding Tasks. If method is post submit form else show the form
@login_required
def add_tasks(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator_id = user
            task.save()
            return redirect('/tasks/')
    else:
        form = AddTaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

#Controller for showing details of task
@login_required
def detail(request, task_id):
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail.html', {'task': task})

#Controller for adding Claiming Tasks
@login_required
def claim(request, task_id):
    user = User.objects.get(username=request.user.username)
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    task.num_workers -= 1
    tuj = TaskUserJunction()
    tuj.worker_id = user
    tuj.task_id = task
    tuj.save()
    task.save()
    return redirect('/tasks/')

#Controller for adding Viewing Claimed Tasks
@login_required
def claimed_tasks(request):
    user = User.objects.get(username=request.user.username)
    tuj_list =TaskUserJunction.objects.filter(worker_id = user)
    context = {
        'tuj_list': tuj_list,
    }
    return render(request, 'tasks/claimed_task.html', context)

#Controller for adding Answer. If method is post submit form else show the form
@login_required
def answer(request, task_id):
    task = ResearchTasks.objects.get(pk=task_id)
    user = User.objects.get(username=request.user.username)
    try:
        tuj = TaskUserJunction.objects.get(worker_id=user, task_id=task)
    except TaskUserJunction.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance = tuj)
        if form.is_valid():
            temp_tuj = form.save(commit=False)
            temp_tuj.submission_time = datetime.now()
            temp_tuj.save()
            return redirect('/tasks/claimed/')
    else:
        form = AnswerForm()
    context = {
        'tuj': tuj,
        'form': form,
        'task' : task,
    }
    return render(request, 'tasks/answer.html', context)