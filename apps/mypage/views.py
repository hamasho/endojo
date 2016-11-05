import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

from core.views import BaseTemplateView, BaseApi
from vocabulary.models import PackageState as VocabularyState
from listening.models import PackageState as ListeningState
from transcription.models import PackageState as TranscriptionState
from registration.forms import UserInfoForm
from registration.models import UserInfo, Language
from .forms import UserForm, PasswordForm


class HomeView(BaseTemplateView):
    template_name = 'mypage/home.html'
    context = {
        'current_page': 'mypage',
        'current_mypage': 'home',
    }


class ScoreApi(BaseApi):
    def get_context_data(self):
        context = {}
        context['vocabulary_score'] = VocabularyState.objects.filter(
            user=self.request.user,
            complete=True,
        ).aggregate(score=Coalesce(Sum('package__level'), 0))['score']
        context['listening_score'] = ListeningState.objects.filter(
            user=self.request.user,
            complete=True,
        ).aggregate(score=Coalesce(Sum('package__level'), 0))['score']
        context['transcription_score'] = TranscriptionState.objects.filter(
            user=self.request.user,
            complete=True,
        ).aggregate(score=Coalesce(Sum('package__level'), 0))['score']
        context['user_score'] = context['vocabulary_score'] + \
            context['listening_score'] + context['transcription_score']
        return context


class HistoryView(BaseTemplateView):
    template_name = 'mypage/history.html'
    context = {
        'current_page': 'mypage',
        'current_mypage': 'history',
    }


class HistoryApi(BaseApi):
    pass


class StatsView(BaseTemplateView):
    template_name = 'mypage/stats.html'
    context = {
        'current_page': 'mypage',
        'current_mypage': 'stats',
    }


class ProfileView(BaseTemplateView):
    template_name = 'mypage/profile.html'

    def get_context_data(self):
        context = super(ProfileView, self).get_context_data()
        context['current_page'] = 'mypage'
        context['current_mypage'] = 'profile'
        context['form'] = UserForm(initial={
            'email': self.request.user.email,
        })
        info = self.request.user.userinfo
        context['info_form'] = UserInfoForm(initial={
            'language': info.language,
            'birth_year': info.birth_date.year,
            'birth_month': info.birth_date.month,
            'birth_day': info.birth_date.day,
        })
        context['pw_form'] = PasswordForm(self.request.user)
        return context

    def post(self, request):
        form = UserForm(request.POST)
        info_form = UserInfoForm(request.POST)
        pw_form = PasswordForm(request.user, request.POST)
        print('------')
        if form.is_valid() and info_form.is_valid() and pw_form.is_valid():
            print('ho')
            with transaction.atomic():
                language = Language.objects.get(
                    language_text=info_form.cleaned_data['language']
                )
                birth_date = datetime.datetime(
                    int(info_form.cleaned_data['birth_year']),
                    int(info_form.cleaned_data['birth_month']),
                    int(info_form.cleaned_data['birth_day']),
                )
                user_info = UserInfo.objects.get(user_id=request.user.id)
                user_info.language = language
                user_info.birth_date = birth_date
                user_info.save()
                user = User.objects.get(pk=request.user.id)
                user.email = form.cleaned_data['email']
                if pw_form.cleaned_data['new_password']:
                    user.set_password(pw_form.cleaned_data['new_password'])
                user.save()
                return redirect(reverse('mypage:profile'))
        else:
            return render(request, self.template_name, {
                'form': form,
                'info_form': info_form,
                'pw_form': pw_form,
            })
