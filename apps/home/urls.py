from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^donate/$', views.DonateView.as_view(), name='donate'),
    url(r'^donate/thanks/$', views.DonateThanksView.as_view(), name='donate_thanks'),
    url(r'^doc/vocabulary/$', views.VocabularyDocumentView.as_view(), name='vocabulary_document'),
    url(r'^doc/listening/$', views.ListeningDocumentView.as_view(), name='listening_document'),
    url(r'^doc/transcription/$', views.TranscriptionDocumentView.as_view(), name='transcription_document'),
]
