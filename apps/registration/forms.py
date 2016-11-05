from datetime import datetime
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
    birth_year = forms.ChoiceField(
        choices=[(y, y) for y in range(1920, datetime.now().year)],
    )
    birth_month = forms.ChoiceField(
        choices=[(m, m) for m in range(1, 13)],
    )
    birth_day = forms.ChoiceField(
        choices=[(d, d) for d in range(1, 32)],
    )
