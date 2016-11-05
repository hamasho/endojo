from django import forms


class UserForm(forms.Form):
    email = forms.EmailField(required=False)


class PasswordForm(forms.Form):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    new_password = forms.CharField(required=False, widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        return super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        old_password = self.cleaned_data.get('password')
        new_password = self.cleaned_data.get('new_password')
        if new_password and not self.user.check_password(old_password):
            self.add_error('password', 'This old password is invalid.')
        else:
            return self.cleaned_data
