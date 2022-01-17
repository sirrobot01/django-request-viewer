from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
# Create your views here.
from request_viewer.models import Logger, ExceptionModel

from django.utils.decorators import method_decorator
from .utils import is_admin, filter_paths
from .conf import LIVE_MONITORING


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class BaseView(generic.ListView):
    paginator = None
    page = 1
    middleware = None
    object_list = None

    def serialize_queryset(self):
        raise NotImplementedError('`serialize_queryset()` must be implemented.')

    def middleware_used(self):
        return self.middleware and self.middleware in settings.MIDDLEWARE

    def get_extra_data(self):
        self.page = self.request.GET.get('page', self.page)
        self.paginator = Paginator(self.serialize_queryset(), 10)

    def get_context_data(self, *args, **kwargs):
        context = super(BaseView, self).get_context_data(*args, **kwargs)
        self.get_extra_data()
        context['paginator'] = self.paginator
        context["is_connected"] = LIVE_MONITORING and self.middleware_used()
        context['object_list'] = self.paginator.page(self.page)
        return context


class RequestDashboard(BaseView):
    template_name = "request_viewer/request.html"
    model = Logger
    paginator = None
    middleware = "request_viewer.middleware.RequestViewerMiddleware"

    def serialize_queryset(self):
        return self.model.get_data()

    def post(self, request, *args, **kwargs):
        self.template_name = "request_viewer/fragments/request/table.html"
        filter_by = request.POST.get('filterBy')
        value = request.POST.get('value')
        page = request.POST.get('page', 1)
        page = 1 if not page else page
        self.get_extra_data()
        paths = filter_paths(self.paginator.page(page), filter_by, value)
        context = super(RequestDashboard, self).get_context_data(*args, **kwargs)
        context["object_list"] = paths
        return render(request, self.template_name, context)


class ExceptionDashboard(BaseView):
    template_name = "request_viewer/exception.html"
    paginator = None
    queryset = ExceptionModel.objects.all()
    middleware = "request_viewer.middleware.ExceptionMiddleware"

    def serialize_queryset(self):
        obj = json.loads(serializers.serialize("json", self.queryset))
        q = [x.get("fields") for x in obj]
        return q

    def post(self, request, **kwargs):
        self.template_name = "request_viewer/fragments/exception/table.html"
        filter_by = request.POST.get('filterBy')
        value = request.POST.get('value')
        page = request.POST.get('page', 1)
        page = 1 if not page else page
        self.get_extra_data()
        exceptions = self.paginator.page(page)
        context = {'exceptions': exceptions, 'is_connected': LIVE_MONITORING}
        return render(request, self.template_name, context)


@csrf_exempt
def get_modal_content(request):
    obj = json.loads(request.POST.get('obj'))
    entity = request.POST.get('entity', "request")
    return render(request, f'request_viewer/fragments/{entity}/modal_content.html', {'obj': obj})
