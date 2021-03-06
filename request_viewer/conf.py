from django.conf import settings

# Request viewer configs
REQUEST_VIEWER = getattr(settings, 'REQUEST_VIEWER', {})
LIVE_MONITORING = REQUEST_VIEWER.get('LIVE_MONITORING', True)
WHITELISTED_PATHS = REQUEST_VIEWER.get('WHITELISTED_PATH', [])
# LOG_EXCEPTIONS = REQUEST_VIEWER.get('LOG_EXCEPTIONS')   @TODO Exception logger
DATETIME_FORMAT = "%d %b %Y %H:%M:%S.%f"

# Static and media files
STATIC_URL = getattr(settings, 'STATIC_URL', '/static/')
MEDIA_URL = getattr(settings, 'MEDIA_URL', '/media/')
