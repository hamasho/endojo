from django.http import JsonResponse

from core.views import BaseTemplateView, BaseListApi
from .models import Package, Problem


class GameView(BaseTemplateView):
    template_name = 'game_transcription/game.html'
    current_page = 'transcription'


class ResultView(BaseTemplateView):
    pass


class PackageListApi(BaseListApi):
    model = Package


class ProblemListApi(BaseListApi):
    model = Problem

    def get(self, request, package_id):
        package = Package.objects.get(id=package_id)
        return JsonResponse(dict(result=list(package.problem_set.values())))
