from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'listening'

urlpatterns = [
    url(r'^$', views.GameView.as_view(), name='game'),

    # Partial HTML files for angular view
    url(r'^packages/select/$', TemplateView.as_view(template_name='listening/select_package.html')),
    url(r'^start/$', TemplateView.as_view(template_name='listening/start.html')),
    url(r'^main/$', TemplateView.as_view(template_name='listening/main.html')),
    url(r'^result/$', TemplateView.as_view(template_name='listening/result.html')),

    # APIs
    url(r'^packages/$', views.PackageListApi.as_view(), name='package_api'),
    url(r'^packages/(?P<package_id>[0-9]+)/problems/$', views.ProblemListApi.as_view(), name='problem_api'),
    url(r'^stats/$', views.StatsApi.as_view(), name='stats_api'),

    url(r'^result/store/$', csrf_exempt(views.ResultStoreApi.as_view()), name='result_store_api'),
]
