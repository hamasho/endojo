from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction

from .models import Language, UserInfo
from .forms import SignUpForm, UserInfoForm


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data()
        context['form'] = SignUpForm()
        context['info_form'] = UserInfoForm()
        return context

    def post(self, request):
        # TODO: username and email must be unique
        form = SignUpForm(request.POST)
        info_form = UserInfoForm(request.POST)
        if form.is_valid() and info_form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                language = Language.objects.get(
                    language_text=info_form.cleaned_data['language']
                )
                UserInfo.objects.create(
                    user=user,
                    language=language,
                    age=info_form.cleaned_data['age'],
                )
            login(request, user)
            return redirect(reverse('home:home'))
        else:
            print(vars(form))
            print(vars(info_form))
            return render(request, self.template_name, {
                'form': form,
                'info_form': info_form,
            })


# TODO: pasword reset
