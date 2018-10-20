from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ResearchTasks

@login_required
def index(request):
    task_list = ResearchTasks.objects.order_by('-creation_time')
    context = {
        'task_list': task_list,
    }
    return render(request, 'tasks/index.html', context)

@login_required
def detail(request, task_id):
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except Question.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail.html', {'task': task})