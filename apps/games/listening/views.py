import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from core.views import BaseTemplateView, BaseListApi
from .models import Package, Problem, ProblemScore, History


class GameView(LoginRequiredMixin, BaseTemplateView):
    template_name = 'listening/game.html'
    context = {'current_page': 'listening'}


class PackageListApi(LoginRequiredMixin, BaseListApi):
    model = Package


class ProblemListApi(LoginRequiredMixin, BaseListApi):
    model = Problem

    def get(self, request, package_id):
        package = Package.objects.get(id=package_id)
        problems = package.problem_set.all()
        result = list(problems.values())
        for i in range(len(result)):
            result[i]['url'] = problems[i].audio_file.url
        return JsonResponse(dict(result=result))


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


class AudioApi(BaseTemplateView):
    pass


class StatsApi(LoginRequiredMixin, BaseListApi):
    def get(self, request):
        return JsonResponse(History.get_formatted_stats(request.user))
