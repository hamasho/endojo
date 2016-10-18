from django.views.generic.base import View, TemplateView
from django.http import JsonResponse


class BaseTemplateView(TemplateView):
    def get_context_data(self):
        context = super(BaseTemplateView, self).get_context_data()
        context['user'] = self.request.user
        try:
            context['current_page'] = self.current_page
        except AttributeError:
            context['current_page'] = None
        return context


class BaseListApi(View):
    # TODO: test
    def get(self, request):
        try:
            objects = self.model.objects.values(*self.values)
        except AttributeError:
            objects = self.model.objects.values()
        return JsonResponse(dict(result=list(objects)))

    # TODO: create
    def post(self, request):
        pass


class BaseDetailApi(View):
    # TODO: implement
    pass
