from django.conf.urls import url

from . import views

app_name = 'mypage'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^history/$', views.HistoryView.as_view(), name='history'),
    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),

    url(r'^score/$', views.ScoreApi.as_view(), name='score_api'),
]
