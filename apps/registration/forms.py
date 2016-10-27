from django import forms
from django.contrib.auth.models import User

from .models import Language


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {'username': None, }
        widgets = {
            'password': forms.PasswordInput,
        }


class UserInfoForm(forms.Form):
    language = forms.ChoiceField(choices=Language.LANGUAGE_CHOICES)
    age = forms.IntegerField()
