from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
# Create your views here.
from request_viewer.models import Logger, Caching

from django.utils.decorators import method_decorator
from .utils import is_admin, filter_paths
from .conf import LIVE_MONITORING
from django.core.cache import cache

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class RequestViewDashboard(generic.ListView):
    template_name = "request_viewer/dashboard.html"
    model = Logger
    paginator = None
    cache = Caching(cache)
    
    def __init__(self):
        super(RequestViewDashboard, self).__init__()
            
    def get_extra_data(self):
        self.paginator = Paginator(self.model.get_data(), 10)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RequestViewDashboard, self).get_context_data(**kwargs)
        self.get_extra_data()
        page = self.request.GET.get('page', 1)
        page = 1 if not page else page
        context['paginator'] = self.paginator
        context['paths'] = self.paginator.page(page)
        context['is_connected'] = LIVE_MONITORING
        context['is_caching'] = self.cache.is_empty
        return context

    def post(self, request, **kwargs):
        self.template_name = "request_viewer/fragments/table.html"
        filter_by = request.POST.get('filterBy')
        value = request.POST.get('value')
        page = request.POST.get('page', 1)
        page = 1 if not page else page
        self.get_extra_data()
        paths = filter_paths(self.paginator.page(page), filter_by, value)
        context = {'paths': paths, 'is_connected': LIVE_MONITORING, 'is_caching': self.cache.is_empty}
        return render(request, self.template_name, context)


@csrf_exempt
def get_modal_content(request):
    path = json.loads(request.POST.get('path'))
    return render(request, 'request_viewer/fragments/modal_content.html', {'path': path})
