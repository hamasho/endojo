from django.db.models import Sum
from django.db.models.functions import Coalesce

from core.views import BaseTemplateView, BaseApi
from vocabulary.models import PackageState as VocabularyState
from listening.models import PackageState as ListeningState
from transcription.models import PackageState as TranscriptionState


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
    context = {
        'current_page': 'mypage',
        'current_mypage': 'profile',
    }
