import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from core.views import BaseTemplateView, BaseListApi
from .models import Package, Problem, ProblemScore, History


class GameView(LoginRequiredMixin, BaseTemplateView):
    template_name = 'transcription/game.html'
    context = {'current_page': 'transcription'}


class PackageListApi(LoginRequiredMixin, BaseListApi):
    model = Package


class ProblemListApi(LoginRequiredMixin, BaseListApi):
    model = Problem

    def get(self, request, package_id):
        package = Package.objects.get(id=package_id)
        return JsonResponse(dict(result=list(package.problem_set.values())))


class ResultStoreApi(LoginRequiredMixin, BaseListApi):
    def post(self, request):
        score = json.loads(request.body.decode())['score']
        for item in score:
            problem_score = ProblemScore(
                user=request.user,
                problem=Problem.objects.get(id=item['id']),
                response_time_ms=item['responseTimeMs']
            )
            problem_score.save()
        return JsonResponse({'status': 'ok'})


class StatsApi(LoginRequiredMixin, BaseListApi):
    def get(self, request):
        return JsonResponse(History.get_formatted_stats(request.user))
