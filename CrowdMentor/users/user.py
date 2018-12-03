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

    return render(request, 'home.html', {'dict_profile': dict_profile})

def user_details(user_id):
    dict_profile = {}
    user = User.objects.get(id=user_id)
    tasks = TaskUserJunction.objects.filter(worker_id_id=user_id)
    dict_profile['id'] = user.id
    dict_profile['fname'] = user.first_name
    dict_profile['lname'] = user.last_name
    dict_profile['username'] = user.username
    dict_profile['email'] = user.email
    dict_profile['role'] = user.profile.role
    dict_profile['bdate'] = user.profile.birth_date
    dict_profile['salary'] = user.profile.salary
    dict_profile['bonus'] = user.profile.bonus
    dict_profile['fine'] = user.profile.fine
    dict_profile['total_salary'] = user.profile.total_salary

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
            id = user.id
            if 'Select' != request.POST.get('role_'+str(id)):
                user.profile.role = request.POST.get('role_'+str(id))
            user.profile.salary = request.POST.get('salary_' + str(id))
            user.profile.bonus = request.POST.get('bonus_' + str(id))
            user.profile.fine = request.POST.get('fine_' + str(id))
            user.profile.audit_prob_user = request.POST.get('audit_prob_' + str(id))
            if request.POST.get('mantor_id_' + str(id)) is not 'None':
                user.profile.mentor_id = request.POST.get('mentor_id_' + str(id))

            user.save()
        return redirect('/')
    user_dict=dict()
    user_dict_html = dict()
    i=0
    for usr in users:
        prf = Profile.objects.get(user_id=usr.id)
        if prf.mentor_id is not None and prf.mentor_id > 0:
            try:
                mentor = User.objects.get(id=prf.mentor_id)
            except User.DoesNotExist:
                mentor = 'None'
            user_dict[usr.id] = [usr.username, usr.email, prf.role, prf.salary, prf.bonus, prf.fine,
                                 prf.audit_prob_user, prf.mentor_id]
            user_dict_html[usr.id] = [usr.username, prf.role, i, i + 1, i + 2, i + 3, i + 4, i+5, mentor]
            i = i + 6
        else:
            user_dict[usr.id] = [usr.username, usr.email, prf.role, prf.salary, prf.bonus, prf.fine,
                                 prf.audit_prob_user,0]
            user_dict_html[usr.id] = [usr.username, prf.role, i, i+1, i+2, i+3, i+4, i+5, 'None']
            i = i + 6

    form = ChangeRolesForm(users=user_dict)
    return render(request, 'changeRoles.html', {'form': form, 'user_dict':user_dict_html})

@login_required
def reset_salary(request,worker_id):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'admin':
        messages.warning(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    worker = User.objects.get(pk=worker_id)
    worker.profile.total_salary = 0.00
    worker.save()
    return redirect('/')
