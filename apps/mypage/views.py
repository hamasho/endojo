from datetime import datetime
import calendar
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

from core.views import BaseTemplateView, BaseApi
from core.utils import month_range, get_today
from vocabulary.models import PackageState as VocabularyState
from listening.models import PackageState as ListeningState
from transcription.models import PackageState as TranscriptionState
from vocabulary.models import History as VocabularyHistory
from listening.models import History as ListeningHistory
from transcription.models import History as TranscriptionHistory
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
    def get_context_data(self):
        context = {}
        context['histories'] = self.get_histories()
        return context

    def get_histories(self):
        vh = VocabularyHistory.objects.filter(user=self.request.user)
        lh = ListeningHistory.objects.filter(user=self.request.user)
        th = TranscriptionHistory.objects.filter(user=self.request.user)
        oldest_date_list = []
        if not vh and not lh and not th:
            return []
        if vh:
            oldest_date_list.append(vh[0].date)
        if lh:
            oldest_date_list.append(lh[0].date)
        if th:
            oldest_date_list.append(th[0].date)
        oldest_date = min(oldest_date_list)
        today = get_today()
        result = []
        for year, month in month_range(oldest_date.year, oldest_date.month, today.year, today.month):
            month_history = []
            for week in calendar.monthcalendar(year, month):
                for day in week:
                    if day == 0:
                        month_history.append({'day': day})
                        continue
                    v_done = vh.filter(date=datetime(year, month, day)).exists()
                    l_done = lh.filter(date=datetime(year, month, day)).exists()
                    t_done = th.filter(date=datetime(year, month, day)).exists()
                    month_history.append({
                        'day': day,
                        'vocabulary': v_done,
                        'listening': l_done,
                        'transcription': t_done,
                    })
            n_vocabulary_words = VocabularyHistory.objects.filter(
                date__year=year,
                date__month=month,
            ).aggregate(n=Coalesce(Sum('n_levelup'), 0))['n']
            n_listening_problems = ListeningHistory.objects.filter(
                date__year=year,
                date__month=month,
            ).aggregate(n=Coalesce(Sum('problem_count'), 0))['n']
            n_transcription_problems = TranscriptionHistory.objects.filter(
                date__year=year,
                date__month=month,
            ).aggregate(n=Coalesce(Sum('problem_count'), 0))['n']
            result.append({
                'year': year,
                'month': month,
                'month_history': month_history,
                'n_vocabulary_words': n_vocabulary_words,
                'n_listening_problems': n_listening_problems,
                'n_transcription_problems': n_transcription_problems,
            })
        result.reverse()
        return result


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
        if form.is_valid() and info_form.is_valid() and pw_form.is_valid():
            with transaction.atomic():
                language = Language.objects.get(
                    language_text=info_form.cleaned_data['language']
                )
                birth_date = datetime(
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
