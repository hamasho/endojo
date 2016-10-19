import json
from django.http import JsonResponse

from core.views import BaseTemplateView, BaseListApi
from .models import Package, Problem, ProblemScore


class GameView(BaseTemplateView):
    template_name = 'transcription/game.html'
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


class ResultStoreApi(BaseListApi):
    def post(self, request):
        score = json.loads(request.body.decode())['score']
        for item in score:
            problem_score, created = ProblemScore.objects.get_or_create(
                user=request.user,
                problem=Problem.objects.get(id=item['id']),
                defaults={
                    'response_time_ms': item['responseTimeMs'],
                }
            )
            problem_score.save()
        return JsonResponse({'status': 'ok'})
