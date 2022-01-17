import os
from datetime import datetime


def is_whitelisted(norm_path, whitelisted_paths=None):
    is_whitelist = False

    if norm_path.endswith('.ico'):
        return True

    if whitelisted_paths is None:
        whitelisted_paths = []

    for path in whitelisted_paths:
        path = '/' + path if not path.startswith('/') else path
        if os.path.normpath(norm_path).startswith(path):
            is_whitelist = True
            break

    return is_whitelist


def get_time_length(request_timestamp, response_timestamp, datetime_format):
    diff = datetime.strptime(response_timestamp, datetime_format) - datetime.strptime(request_timestamp,
                                                                                      datetime_format)
    return diff.total_seconds()


# View utils

def is_admin(user):
    return user.is_superuser


def filter_paths(paths, filter_by, value):
    if filter_by == "method":
        if value:
            return [path for path in paths if path.get('method') == value]
        else:
            return paths
    else:
        if value:
            return [path for path in paths if any([value.lower() in [str(val).lower() for val in path.values()]])]
        else:
            return paths
