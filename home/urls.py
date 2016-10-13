from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='home/about.html'), name='about'),
    url(r'^donate/$', views.DonateView.as_view(), name='donate'),
    url(r'^donate/thanks/$', TemplateView.as_view(template_name='home/donate_thanks.html'), name='donate_thanks'),
    url(r'^doc/vocabulary/$', TemplateView.as_view(template_name='home/vocabulary_document.html'), name='vocabulary_document'),
    url(r'^doc/listening/$', TemplateView.as_view(template_name='home/listening_document.html'), name='listening_document'),
    url(r'^doc/transcription/$', TemplateView.as_view(template_name='home/transcription_document.html'), name='transcription_document'),
]
