from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

app_name = 'game_transcription'

urlpatterns = [
    url(r'^$', views.GameView.as_view(), name='game'),
    url(r'^packages/$', views.PackageListApi.as_view(), name='transcription_game_package_api'),
    url(r'^packages/(?P<package_id>[0-9]+)/problems/$', views.ProblemListApi.as_view(), name='transcription_game_problem_api'),
    url(r'^packages/select/$', TemplateView.as_view(template_name='game_transcription/select_package.html')),
    url(r'^start/$', TemplateView.as_view(template_name='game_transcription/start.html')),
]
