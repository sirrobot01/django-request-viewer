from django.urls import path
from .views import RequestDashboard, ExceptionDashboard, get_modal_content

urlpatterns = [
    path('request-viewer/', RequestDashboard.as_view(), name="request-viewer"),
    path('request-viewer/exceptions', ExceptionDashboard.as_view(), name="exception-viewer"),
    path('modal-content/', get_modal_content, name='modal-content')
]
