from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class AboutView(TemplateView):
    template_name = 'home/about.html'


class DonateView(TemplateView):
    template_name = 'home/donate.html'


class DonateThanksView(TemplateView):
    template_name = 'home/donate_thanks.html'
