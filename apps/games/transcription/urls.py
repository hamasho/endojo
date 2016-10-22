from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

app_name = 'transcription'

urlpatterns = [
    url(r'^$', views.GameView.as_view(), name='game'),

    # Partial HTML files for angular view
    url(r'^packages/select/$', TemplateView.as_view(template_name='transcription/select_package.html')),
    url(r'^start/$', TemplateView.as_view(template_name='transcription/start.html')),
    url(r'^main/$', TemplateView.as_view(template_name='transcription/main.html')),
    url(r'^result/$', TemplateView.as_view(template_name='transcription/result.html')),

    # APIs
    url(r'^packages/$', views.PackageListApi.as_view(), name='package_api'),
    url(r'^packages/(?P<package_id>[0-9]+)/problems/$', views.ProblemListApi.as_view(), name='problem_api'),
    url(r'^stats/$', views.StatsApi.as_view(), name='stats_api'),

    url(r'^result/store/$', views.ResultStoreApi.as_view(), name='result_store_api'),
]
