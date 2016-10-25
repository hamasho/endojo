from django.contrib.auth.mixins import LoginRequiredMixin

from core.views import BaseTemplateView, BaseListApi
from .models import Package, Word


class GameView(LoginRequiredMixin, BaseTemplateView):
    template_name = 'listening/game.html'
    context = {'current_page': 'listening'}


class PackageListApi(LoginRequiredMixin, BaseListApi):
    model = Package


class WordListApi(LoginRequiredMixin, BaseListApi):
    model = Word

    def get(self, request, package_id):
        pass


class MarkedWordStoreApi(LoginRequiredMixin, BaseListApi):
    def post(self, request):
        pass


class ResultStoreApi(LoginRequiredMixin, BaseListApi):
    def post(self, request):
        pass


class StatsApi(LoginRequiredMixin, BaseListApi):
    def get(self, request):
        pass
