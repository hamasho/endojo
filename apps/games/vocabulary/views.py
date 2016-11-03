import json
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse

from core.views import BaseTemplateView, BaseApi
from .models import Package, Word, PackageState, WordState


class GameView(BaseTemplateView):
    template_name = 'vocabulary/game.html'
    context = {'current_page': 'vocabulary'}


class PackageSelectView(BaseTemplateView):
    template_name = 'vocabulary/select_package.html'
    context = {'current_page': 'vocabulary'}

    def get_context_data(self):
        context = {
            'n_learning_words': WordState.objects.filter(
                user=self.request.user,
                state__lte=5,
            ).count(),
            'n_todays_words': WordState.objects.filter(
                user=self.request.user,
                state__lte=5,
                next_date__lte=timezone.now(),
            ).count(),
        }
        return context


class PackageListApi(BaseApi):
    def get_context_data(self):
        return {
            'packages': Package.get_package_list(
                user=self.request.user,
                language=self.request.user.userinfo.language,
            )
        }


class WordListApi(BaseApi):
    def get_context_data(self):
        return {
            'words': Word.get_translated_words(
                self.kwargs['package_id'],
                self.request.user.userinfo.language,
            )
        }


class LearningWordListApi(BaseApi):
    def get_context_data(self):
        words = WordState.get_learning_words(self.request.user, 10)
        return {'words': words}


class UnknownWordsStoreApi(BaseApi):
    def post(self, request):
        json_data = json.loads(request.body.decode())
        package = json_data['package']
        unknown_words = json_data['words']
        with transaction.atomic():
            WordState.objects.filter(
                user=request.user,
                word__package_id=package['id'],
            ).delete()
            for word in unknown_words:
                state, created = WordState.objects.get_or_create(
                    user=request.user,
                    word_id=word['id'],
                )
                state.save()
            complete = len(unknown_words) == 0
            PackageState.objects.update_or_create(
                user=request.user,
                package_id=package['id'],
                defaults={'complete': complete}
            )
        return JsonResponse({'status': 'ok'})


class ResultStoreApi(BaseApi):
    def post(self, request):
        json_data = json.loads(request.body.decode())
        for word in json_data['failed']:
            state = WordState.objects.get(id=word['id'])
            state.level_reset()
        for word in json_data['answered']:
            state = WordState.objects.get(id=word['id'])
            state.level_up()
        return JsonResponse({'status': 'ok'})


class StatsApi(BaseApi):
    def get(self, request):
        pass
