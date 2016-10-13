from django.views.generic.base import TemplateView


class BaseTemplateView(TemplateView):
    def get_context_data(self):
        context = super(BaseTemplateView, self).get_context_data()
        context['user'] = self.request.user
        try:
            context['current_page'] = self.current_page
        except AttributeError:
            context['current_page'] = None
        return context
