from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profile import Profile
from UserRoles import UserRoles
from changeRolesForm import ChangeRolesForm


@login_required
def view(request):
    user_id = User.objects.get(username=request.user.username).id
    profile = Profile.objects.get(user_id=user_id).role
    dict_functs={'/tasks/': 'View open tasks', '/tasks/claimed': 'View claimed tasks'}
    if profile == UserRoles.TASK_UPDATER.value or profile == UserRoles.ADMIN.value:
        dict_functs['/tasks/add_tasks']= 'Add task'
        dict_functs['/change_roles'] = 'Change user roles'

    return render(request, 'home.html', {"profile": profile, "dict_functs" : dict_functs})


def change_roles(request):
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