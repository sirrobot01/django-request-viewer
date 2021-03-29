from django.db import models
import json
from django.conf import settings
from django.http import HttpRequest
from datetime import datetime

from .conf import DATETIME_FORMAT
try:
    from django.db.models import JSONField
except ModuleNotFoundError:
    from django.contrib.postgres.fields import JSONField


# Create your models here.


class Logger(models.Model):
    path = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(default=list)
    
    @classmethod
    def get_data(cls, filter_by=None, value=None):
        data = []
        logs = cls.objects.all()
        for log in logs:
            log_data = log.data
            data.extend(log_data)
        return data


class BaseClass:
    
    def to_json(self):
        return json.dumps(self.__dict__)


class RequestModel(BaseClass):
    LOG_EXCEPTIONS = getattr(settings, "LOG_EXCEPTIONS", False)

    def __init__(self, request: HttpRequest):
        self.path = request.path
        self.method = request.method
        self.request_timestamp = datetime.now().strftime(DATETIME_FORMAT)
        self.params = dict(request.GET) if self.method == "GET" else dict(request.POST)
        self.files = dict(request.FILES)
        self.headers = dict(request.headers)
        self.authenticated_request = request.user.is_authenticated

    def get_object(self):
        return self.__class__(**self.__dict__)
    
    @property
    def __dict__(self):
        return {
            "path": self.path,
            "method": self.method,
            "params": self.params,
            "files": self.files,
            "headers": self.headers,
            "request_timestamp": self.request_timestamp
        }


class BaseResponse(BaseClass):
    
    def __init__(self, response):
        self.status_code = response.status_code
        self.status_message = response.reason_phrase
        self.content_type = response.charset
        self.response_datetime = datetime.now().strftime(DATETIME_FORMAT)
        super(BaseResponse, self).__init__()
    
    @property
    def __dict__(self):
        return {
            "status_code": self.status_code,
            "status_message": self.status_message,
            "content_type": self.content_type,
            "response_timestamp": self.response_datetime
        }
    

class ResponseModel(BaseResponse):

    def __init__(self, response):
        if isinstance(response.content, bytes):
            self.message = response.content.decode()
        else:
            self.message = response.content
        super(ResponseModel, self).__init__(response)
    
    @property
    def __dict__(self):
        return dict(super(ResponseModel, self).__dict__, **{"message": self.message})

class TemplateResponseModel(BaseResponse):

    def __init__(self, response):
        self.template_name = response.template_name
        context_data = response.context_data
        self.view = str(context_data.get('view'))
        super(TemplateResponseModel, self).__init__(response)
    
    @property
    def __dict__(self):
        data = {
            "template_name": self.template_name,
            "view": self.view
        }
        return dict(super(TemplateResponseModel, self).__dict__, **data)

