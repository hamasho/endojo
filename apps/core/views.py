from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class BaseTemplateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self):
        context = super(BaseTemplateView, self).get_context_data()
        context['user'] = self.request.user
        extras = getattr(self, 'context', {})
        context = dict(list(context.items()) + list(extras.items()))
        return context


class BaseApi(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return JsonResponse(context)
