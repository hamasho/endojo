from core.views import BaseTemplateView


class HomeView(BaseTemplateView):
    template_name = 'mypage/home.html'
    context = {
        'current_page': 'mypage',
        'current_mypage': 'home',
    }


class HistoryView(BaseTemplateView):
    template_name = 'mypage/history.html'
    context = {
        'current_page': 'mypage',
        'current_mypage': 'history',
    }


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
