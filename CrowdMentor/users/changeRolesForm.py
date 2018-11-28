from django import forms
import UserRoles
from django.contrib.auth.models import User

class ChangeRolesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users')  # user was passed to a single form
        super(ChangeRolesForm, self).__init__(*args, **kwargs)

        for key, value in self.users.iteritems():
            label= ''
            choices = [(tag.value, tag.value) for tag in UserRoles.UserRoles]
            choices.insert(0, ('Select', 'Select'));
            self.fields['role_'+str(key)] = forms.ChoiceField(choices=choices, label=label, required=False)
            self.fields['salary_'+str(key)] = forms.FloatField(label='Salary', initial=value[3], required=False)
            self.fields['bonus_' + str(key)] = forms.FloatField(label='Bonus', initial=value[4], required=False)
            self.fields['fine_' + str(key)] = forms.FloatField(label='Fine', initial=value[5], required=False)
            self.fields['audit_prob_' + str(key)] = forms.FloatField(label='Audit Probability', initial=value[6], required=False)
            #self.fields['mantor_id_' + str(key)] = forms.IntegerField(label='Mentor id', initial=value[7], required=False)
            self.fields['mentor_id_' + str(key)] = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
            # self.fields['role_' + str(key)].initial = value[2]


