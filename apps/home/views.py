from django.shortcuts import render, redirect
from django.urls import reverse

from core.views import BaseNoLoginTemplateView
from home.forms import ContactForm


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


class ContactView(BaseNoLoginTemplateView):
    template_name = 'home/contact.html'

    def get_context_data(self):
        return {
            'form': ContactForm(initial={}),
        }

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['contact_name'])
            print(form.cleaned_data['contact_email'])
            print(form.cleaned_data['contact_text'])
            return redirect(reverse('home:home'))
        else:
            return render(request, self.template_name, {
                'form': form,
            })
