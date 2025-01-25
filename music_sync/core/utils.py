import os
from urllib.parse import urlparse


def get_absolute_path(value, base_path=None):
    value = os.path.expandvars(value)
    value = os.path.expanduser(value)
    if os.path.isabs(value):
        return value
    if base_path is not None:
        value = os.path.join(get_absolute_path(base_path), value)
    return os.path.abspath(value)


def safe_issubclass(*arg, **kwargs):
    try:
        return issubclass(*arg, **kwargs)
    except Exception:
        return False


def is_valid_url(url, qualifying=("scheme", "netloc")):
    tokens = urlparse(url)
    return all([getattr(tokens, qualifying_attr) for qualifying_attr in qualifying])
