from django.views.generic.base import TemplateView


class DonateView(TemplateView):
    template_name = 'home/donate.html'
