from django import forms

MY_CHOICES = (
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
)

class ChangeRolesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users')  # user was passed to a single form
        super(ChangeRolesForm, self).__init__(*args, **kwargs)

        for key, value in self.users.iteritems():
            label= 'username:'+value[0]+' role:'
            help='email:'+value[1]
            self.fields['role_'+str(key)] = forms.ChoiceField(choices=MY_CHOICES, label=label, required=False,help_text=help)


