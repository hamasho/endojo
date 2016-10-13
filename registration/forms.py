from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {'username': None, }
        widgets = {
            'password': forms.PasswordInput,
        }

    def is_valid(self):
        valid = super(SignUpForm, self).is_valid()

        if self.cleaned_data.get('username') == '':
            self.errors.setdefault('username', []).append('Username is required.')
            valid = False

        if self.cleaned_data.get('email') == '':
            self.errors.setdefault('email', []).append('Email address is required.')
            valid = False

        if self.cleaned_data.get('password') == '':
            self.errors.setdefault('password', []).append('Password is required.')
            valid = False

        return valid
