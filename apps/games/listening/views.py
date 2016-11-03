import json
from django.http import JsonResponse

from core.views import BaseTemplateView, BaseApi
from .models import Package, PackageState, Problem, ProblemScore, History


class GameView(BaseTemplateView):
    template_name = 'listening/game.html'
    context = {'current_page': 'listening'}


class PackageListApi(BaseApi):
    def get_context_data(self):
        return {
            'packages': Package.get_package_list(
                user=self.request.user,
            )
        }


class ProblemListApi(BaseApi):
    def get_context_data(self):
        package = Package.objects.get(id=self.kwargs['package_id'])
        problems = package.problem_set.all()
        result = list(problems.values())
        for i in range(len(result)):
            result[i]['url'] = problems[i].audio_file.url
        return {'problems': result}


class ResultStoreApi(BaseApi):
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
                    complete=True,
                )
            else:
                package_completed = False
                problem_score = ProblemScore(
                    user=request.user,
                    problem=Problem.objects.get(id=item['id']),
                    complete=False,
                )
            problem_score.save()

        PackageState.objects.update_or_create(
            user=request.user,
            package_id=json_data['package']['id'],
            defaults={'complete': package_completed},
        )

        return JsonResponse({'status': 'ok'})


class StatsApi(BaseApi):
    def get(self, request):
        return JsonResponse(History.get_formatted_stats(request.user))
