from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from . import forms


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data()
        context['form'] = forms.SignUpForm()
        return context

    def post(self, request):
        # TODO: username and email must be unique
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect(reverse('home:home'))
        else:
            return render(request, self.template_name, {
                'form': form,
            })


# TODO: pasword reset
