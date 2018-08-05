from django import forms

from registration.forms import RegistrationForm

from backend.core.models import EmailBasedUser


class EmailBasedUserForm(RegistrationForm):
    recaptcha = forms.BooleanField(widget=forms.HiddenInput, required=False)

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'recaptcha']
        model = EmailBasedUser

    def __init__(self, *args, **kwargs):
        super(EmailBasedUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
