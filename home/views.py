from core.views import BaseTemplateView


class HomeView(BaseTemplateView):
    template_name = 'home/home.html'


class AboutView(BaseTemplateView):
    template_name = 'home/about.html'


class DonateView(BaseTemplateView):
    template_name = 'home/donate.html'


class DonateThanksView(BaseTemplateView):
    template_name = 'home/donate_thanks.html'


class VocabularyDocumentView(BaseTemplateView):
    template_name = 'home/vocabulary_document.html'


class ListeningDocumentView(BaseTemplateView):
    template_name = 'home/listening_document.html'


class TranscriptionDocumentView(BaseTemplateView):
    template_name = 'home/transcription_document.html'
