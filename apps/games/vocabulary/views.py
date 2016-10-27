import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from core.views import BaseTemplateView, BaseListApi, BaseApi
from .models import Package, Word, WordState, TranslatedWord


class GameView(LoginRequiredMixin, BaseTemplateView):
    template_name = 'vocabulary/game.html'
    context = {'current_page': 'vocabulary'}


class PackageListApi(LoginRequiredMixin, BaseApi):
    def get(self, request):
        packages = Package.objects.filter(
            availablepackage__language=request.user.userinfo.language,
        )
        return JsonResponse(dict(result=list(packages.values())))


class WordListApi(LoginRequiredMixin, BaseListApi):
    model = Word

    def get(self, request, package_id):
        package = Package.objects.get(id=package_id)
        translated_words = TranslatedWord.objects.filter(
            word__package=package
        )
        result = []
        for translated_word in translated_words:
            result.append(dict(
                id=translated_word.word.id,
                word_text=translated_word.word.word_text,
                meaning=translated_word.meaning,
            ))
        return JsonResponse(dict(result=result))


class LearningWordListApi(LoginRequiredMixin, BaseApi):
    def get(self, request):
        words = WordState.get_learning_words(request.user, 10)
        return JsonResponse({'result': words})


class UnknownWordsStoreApi(LoginRequiredMixin, BaseListApi):
    def post(self, request):
        words = json.loads(request.body.decode())['words']
        for word in words:
            state, created = WordState.objects.get_or_create(
                user=request.user,
                word_id=int(word['id']),
            )
            state.save()
        return JsonResponse({'status': 'ok'})


class ResultStoreApi(LoginRequiredMixin, BaseListApi):
    def post(self, request):
        result = json.loads(request.body.decode())['result']
        for item in result:
            vars(item)
        return JsonResponse({'status': 'ok'})


class StatsApi(LoginRequiredMixin, BaseListApi):
    def get(self, request):
        pass
