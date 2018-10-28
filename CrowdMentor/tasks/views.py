import random

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

from .models import ResearchTasks, TaskUserJunction, Audit

from .forms import AddTaskForm, AnswerForm, AuditForm

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
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'task_updater':
        return render(request, 'tasks/permission_denied.html')
    if request.method == 'POST':
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
    user = User.objects.get(username=request.user.username)
    claim_permission = user.profile.role == 'worker'
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail.html', {'task': task, 'claim_permission': claim_permission})

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
            if temp_tuj.task_id.audit_by == 1:
                audit_prob = temp_tuj.task_id.audit_prob
            else:
                audit_prob = temp_tuj.worker_id.profile.audit_prob_user
            if random.random() <= audit_prob:
                audit = Audit()
                audit.task_id = task
                audit.save()
            return redirect('/tasks/claimed/')
    else:
        form = AnswerForm()
    context = {
        'tuj': tuj,
        'form': form,
        'task' : task,
    }
    return render(request, 'tasks/answer.html', context)

@login_required
def open_audits(request):
    audit_list = Audit.objects.filter(auditor_id=None)
    context = {
        'audit_list': audit_list,
    }
    return render(request, 'tasks/open_audit.html', context)

def detail_audit(request, task_id):
    try:
        task = ResearchTasks.objects.get(pk=task_id)
        audit_tasks = Audit.objects.get(task_id = task)
        tuj = TaskUserJunction.objects.get(task_id=task)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail_audit.html', {'audit_task': audit_tasks, 'tuj': tuj})

@login_required
def claim_audit(request, task_id):
    user = User.objects.get(username=request.user.username)
    try:
        task = ResearchTasks.objects.get(pk=task_id)
        audit_tasks = Audit.objects.get(task_id=task)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    audit_tasks.auditor_id = user
    audit_tasks.start_time = datetime.now()
    audit_tasks.save()
    return redirect('/tasks/')

@login_required
def audit_tasks(request):
    user = User.objects.get(username=request.user.username)
    audit_list =Audit.objects.filter(auditor_id = user)
    context = {
        'audit_list': audit_list,
    }
    return render(request, 'tasks/audit_list.html', context)

@login_required
def submit_audit(request, task_id):
    task = ResearchTasks.objects.get(pk=task_id)
    user = User.objects.get(username=request.user.username)
    try:
        tuj = TaskUserJunction.objects.get(task_id=task)
        audit_task = Audit.objects.get(auditor_id=user, task_id=task)
    except TaskUserJunction.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        form = AuditForm(request.POST, instance = audit_task)
        if form.is_valid():
            temp_audit_task = form.save(commit=False)
            temp_audit_task.finish_time = datetime.now()
            temp_audit_task.save()
            return redirect('/tasks/audits/')
    else:
        form = AuditForm()
    context = {
        'audit_task': audit_task,
        'form': form,
        'tuj' : tuj,
    }
    return render(request, 'tasks/submit_audit.html', context)