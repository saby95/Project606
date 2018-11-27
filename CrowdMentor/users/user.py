from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profile import Profile
from UserRoles import UserRoles
from changeRolesForm import ChangeRolesForm
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime
from tasks.models import TaskUserJunction

@login_required
def view(request):
    user_id = User.objects.get(username=request.user.username).id
    profile = Profile.objects.get(user_id=user_id).role

    dict_profile = {}
    if profile == UserRoles.WORKER.value:
        dict_profile[request.user.username] = user_details(user_id)
    elif profile == UserRoles.MENTOR.value:
        workers = Profile.objects.filter(mentor_id=user_id)
        for worker in workers:
            profile_val = user_details(worker.user_id)
            dict_profile[profile_val['username']] = profile_val
    elif profile == UserRoles.ADMIN.value:
        workers = Profile.objects.all()
        for worker in workers:
            if worker.role == 'worker':
                profile_val = user_details(worker.user_id)
                dict_profile[profile_val['username']] = profile_val

    return render(request, 'home.html', {"profile": profile, 'dict_profile': dict_profile})

def user_details(user_id):
    dict_profile = {}
    user = User.objects.get(id=user_id)
    tasks = TaskUserJunction.objects.filter(worker_id_id=user_id)
    dict_profile['fname'] = user.first_name
    dict_profile['lname'] = user.last_name
    dict_profile['username'] = user.username
    dict_profile['role'] = user.email
    dict_profile['bdate'] = user.profile.birth_date
    dict_profile['salary'] = user.profile.salary
    dict_profile['bonus'] = user.profile.bonus
    dict_profile['fine'] = user.profile.fine

    total_task = 0
    task_in_progress = 0
    time_worked = datetime.datetime.now()
    for task in tasks:
        total_task = total_task + 1
        if task.submission_time is None:
            task_in_progress = task_in_progress + 1
        else:
            time_worked = time_worked + (task.submission_time - task.claim_time)
    dict_profile['claimed'] = total_task
    dict_profile['finished'] = (total_task - task_in_progress)
    dict_profile['worked'] = max((time_worked-datetime.datetime.now()).total_seconds()/3600,0)
    try:
        dict_profile['avgworked'] = (dict_profile['worked'] / dict_profile['finished'])
    except:
        dict_profile['avgworked'] = 0

    return dict_profile

@login_required
def change_roles(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'admin':
        messages.warning(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')

    users = User.objects.all()
    if request.method == 'POST':
        for user in users:
            id = 'role_'+str(user.id)
            if 'Select' != request.POST.get(id):
                user.profile.role = request.POST.get(id)
                user.save()
        return redirect('/')
    user_dict=dict()
    for usr in users:
        prf = Profile.objects.get(user_id=usr.id)
        user_dict[usr.id] = [usr.username, usr.email, prf.role]
    form = ChangeRolesForm(users=user_dict)
    return render(request, 'changeRoles.html', {'form': form, 'user_dict':user_dict})