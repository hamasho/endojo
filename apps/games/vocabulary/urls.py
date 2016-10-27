from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'vocabulary'

urlpatterns = [
    url(r'^$', views.GameView.as_view(), name='game'),

    # Partial HTML files for angular view
    url(r'^packages/select/$', TemplateView.as_view(template_name='vocabulary/select_package.html')),
    url(r'^packages/words/select/$', TemplateView.as_view(template_name='vocabulary/word_select.html')),
    url(r'^start/$', TemplateView.as_view(template_name='vocabulary/start.html')),
    url(r'^main/$', TemplateView.as_view(template_name='vocabulary/main.html')),
    url(r'^result/$', TemplateView.as_view(template_name='vocabulary/result.html')),

    # APIs
    url(r'^packages/$', views.PackageListApi.as_view(), name='package_api'),
    url(r'^packages/(?P<package_id>[0-9]+)/words/$', views.WordListApi.as_view(), name='word_api'),
    url(r'^words/learning/$', views.LearningWordListApi.as_view(), name='learning_word_api'),
    url(r'^stats/$', views.StatsApi.as_view(), name='stats_api'),

    url(r'^words/unknown/$', csrf_exempt(views.UnknownWordsStoreApi.as_view()), name='unknown_words_store_api'),
    url(r'^result/store/$', csrf_exempt(views.ResultStoreApi.as_view()), name='result_store_api'),
]
