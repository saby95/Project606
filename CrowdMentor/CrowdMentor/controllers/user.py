from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from CrowdMentor.models import Profile
from CrowdMentor.utilities.UserRoles import UserRoles

# dict_roles= {'UserRoles.WORKER': 'worker', 'UserRoles.TASK_UPDATER': 'task_updater', 'UserRoles.AUDITOR': 'auditor',
#              'UserRoles.ADMIN': 'admin', 'UserRoles.MENTOR': 'mentor'}


@login_required
def view(request):
    user_id = User.objects.get(username=request.user.username).id
    profile = Profile.objects.get(user_id=user_id).role
    dict_functs={'/tasks/': 'View open tasks', '/tasks/claimed': 'View claimed tasks'}
    if profile == UserRoles.TASK_UPDATER or profile == UserRoles.ADMIN:
        dict_functs['/tasks/add_tasks']= 'Add task'
        dict_functs['/change_roles'] = 'Change user roles'

    return render(request, 'home.html', {"profile": profile, "dict_functs" : dict_functs})

@login_required
def change_roles(request):
    if request.method == 'PUT':
        # CHANGE these to actual user id and UserRole value from the request parameters
        user = User.objects.get(username=request.user.username)
        user.profile.role = UserRoles.WORKER
        user.save()
    return render(request, 'changeRoles.html')