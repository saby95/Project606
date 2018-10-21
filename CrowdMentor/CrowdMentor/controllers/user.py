from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from CrowdMentor.models import Profile
from CrowdMentor.utilities.changeRolesForm import ChangeRolesForm

dict_roles= {'UserRoles.WORKER': 'worker', 'UserRoles.TASK_UPDATER': 'task_updater', 'UserRoles.AUDITOR': 'auditor',
             'UserRoles.ADMIN': 'admin', 'UserRoles.MENTOR': 'mentor'}


@login_required
def view(request):
    user_id = User.objects.get(username=request.user.username).id
    profile = dict_roles[Profile.objects.get(user_id=user_id).role]
    dict_functs={'/tasks/': 'View open tasks', '/tasks/claimed': 'View claimed tasks'}
    if profile == 'task_updater' or profile == 'admin':
        dict_functs['/tasks/add_tasks']= 'Add task'
        dict_functs['/change_roles'] = 'Change user roles'

    return render(request, 'home.html', {"profile": profile, "dict_functs" : dict_functs})

@login_required
def change_roles(request):
    users= User.objects.all()
    user_dict=dict()
    for usr in users:
        prf = Profile.objects.get(user_id=usr.id)
        user_dict[usr.id] = [usr.username, usr.email, prf.role]
    form = ChangeRolesForm(request.POST, users=user_dict)
    return render(request, 'changeRoles.html', {'form': form})