from django import forms
import UserRoles

class ChangeRolesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users')  # user was passed to a single form
        super(ChangeRolesForm, self).__init__(*args, **kwargs)

        for key, value in self.users.iteritems():
            label= 'username:'+value[0]+' role:'
            help='email:'+value[1]
            choices = [(tag.value, tag.value) for tag in UserRoles.UserRoles]
            choices.insert(0, ('Select', 'Select'));
            self.fields['role_'+str(key)] = forms.ChoiceField(choices=choices, label=label, required=False)
            # self.fields['role_' + str(key)].initial = value[2]


