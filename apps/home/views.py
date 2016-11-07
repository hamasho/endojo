from core.views import BaseNoLoginTemplateView


class HomeView(BaseNoLoginTemplateView):
    template_name = 'home/home.html'
    context = {'current_page': 'home'}


class AboutView(BaseNoLoginTemplateView):
    template_name = 'home/about.html'


class DonateView(BaseNoLoginTemplateView):
    template_name = 'home/donate.html'


class DonateThanksView(BaseNoLoginTemplateView):
    template_name = 'home/donate_thanks.html'


class VocabularyDocumentView(BaseNoLoginTemplateView):
    template_name = 'home/vocabulary_document.html'
    context = {'current_page': 'vocabulary_document'}


class ListeningDocumentView(BaseNoLoginTemplateView):
    template_name = 'home/listening_document.html'
    context = {'current_page': 'listening_document'}


class TranscriptionDocumentView(BaseNoLoginTemplateView):
    template_name = 'home/transcription_document.html'
    context = {'current_page': 'transcription_document'}
