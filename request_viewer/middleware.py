from django.template.response import TemplateResponse
from django.urls import reverse
from django.conf import settings
import os, traceback

from .models import RequestModel, ResponseModel, Logger, TemplateResponseModel, ExceptionModel
from .conf import WHITELISTED_PATHS, DATETIME_FORMAT, LIVE_MONITORING
from .utils import is_whitelisted, get_time_length

default_whitelist = [
    os.path.normpath(path) for path in [reverse('request-viewer'),
                                        reverse('modal-content'), settings.MEDIA_URL, settings.STATIC_URL]]

WHITELISTED_PATHS.extend(default_whitelist)


class RequestViewerMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_obj = {}
        self.response_obj = {}

    def __call__(self, request):
        path = request.path
        if not is_whitelisted(os.path.normpath(path), WHITELISTED_PATHS) and LIVE_MONITORING:
            self.request_obj = RequestModel(request).__dict__
            obj, _ = Logger.objects.get_or_create(path=path)
            response = self.get_response(request)
            if isinstance(response, TemplateResponse):
                self.response_obj = TemplateResponseModel(response).__dict__
            else:
                self.response_obj = ResponseModel(response).__dict__
            old_data = obj.data
            time_length = get_time_length(self.request_obj.get('request_timestamp'), self.response_obj.get('response_timestamp'), DATETIME_FORMAT)
            self.request_obj['time_length'] = time_length
            parsed_data = dict(self.request_obj, **self.response_obj)
            if parsed_data not in old_data:
                old_data.append(parsed_data)

            obj.data = old_data
            obj.save()

        return self.get_response(request)

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        path = request.path
        if not is_whitelisted(os.path.normpath(path), WHITELISTED_PATHS) and LIVE_MONITORING:
            self.run_exception(exception)
    
    @staticmethod
    def run_exception(exception):
        tb = exception.__traceback__
        
        traces = traceback.extract_tb(tb)
        
        exec_type = type(exception).__name__
        stacks = []
        for frame in traces:
            stack = {
                'filename': frame.filename,
                'lineno': frame.lineno,
                'name': frame.name,
                'line': frame.line,
                'locals': frame.locals
            }
            stacks.append(stack)
        if hasattr(exception, "message"):
            message = exception.message
        else:
            message = None
        
        last_stack = stacks[-1] if stacks else {}
        obj = ExceptionModel(
            func_name=last_stack.get("name"),
            line_no=last_stack.get("lineno"),
            line=last_stack.get("line"),
            exc_type=exec_type,
            message=message,
            stacks=stacks
        )
        obj.save()
