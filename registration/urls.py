from django.conf.urls import url
from django.contrib.auth import views

from .views import SignUpView

app_name = 'registration'

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # TODO: password reset
]
