import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from core.views import BaseTemplateView, BaseListApi
from .models import Package, PackageState, Problem, ProblemScore, History


class GameView(LoginRequiredMixin, BaseTemplateView):
    template_name = 'listening/game.html'
    context = {'current_page': 'listening'}


class PackageListApi(LoginRequiredMixin, BaseListApi):
    def get(self, request):
        packages = Package.objects.values()
        for package in packages:
            package['n_tried'] = PackageState.objects.filter(
                package_id=package['id'],
            ).count()
            package['n_completed'] = PackageState.objects.filter(
                package_id=package['id'],
                complete=True,
            ).count()
        return JsonResponse(dict(packages=list(packages)))


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
        json_data = json.loads(request.body.decode())
        score = json_data['score']
        package_completed = True
        for item in score:
            if item['complete']:
                problem_score = ProblemScore(
                    user=request.user,
                    problem=Problem.objects.get(id=item['id']),
                    response_time_ms=item['responseTimeMs'],
                    complete=item['complete'],
                )
            else:
                package_completed = False
                problem_score = ProblemScore(
                    user=request.user,
                    problem=Problem.objects.get(id=item['id']),
                    complete=item['complete'],
                )
            problem_score.save()

        PackageState.objects.update_or_create(
            user=request.user,
            package_id=json_data['package']['id'],
            defaults={'complete': package_completed},
        )

        return JsonResponse({'status': 'ok'})


class AudioApi(BaseTemplateView):
    pass


class StatsApi(LoginRequiredMixin, BaseListApi):
    def get(self, request):
        return JsonResponse(History.get_formatted_stats(request.user))
