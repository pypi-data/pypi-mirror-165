import time
from urllib import parse
from threading import Thread
from functools import wraps
from django.urls import get_resolver, path, re_path
from django.conf import settings as django_settings

DJANGO_URL = {}

def get_setting():
    return getattr(django_settings, 'DJANGO_URL', {})

def get_objs_all_attr(objs, attr, ls=[]):
    for obj in objs:
        try:
            ls.append(getattr(obj, attr))
        except AttributeError:
            pass
    return ls

def url_pattern(url_path, isregex=False, **kwargs):  # url_path, isregex, name(template_name)
    def middle(func):
        @wraps(func)
        def inner(request, *args, **innerkwargs):
            result = func(request, *args, **innerkwargs)
            return result
        if not hasattr(url_pattern, "_all_func"):
            url_pattern._all_func = []
        context = {}
        context['url_path'] = url_path
        context['isregex'] = isregex
        context['func'] = func
        context['name'] = kwargs.get('name') or func.__name__
        url_pattern._all_func.append(context)
        return inner
    return middle

def set_path():
    apps_route_prefix = get_setting()
    if not hasattr(url_pattern, '_all_func'):
        url_pattern._all_func = []
    url_patterns = get_resolver().url_patterns
    for c in url_pattern._all_func:
        url_path = c.get('url_path')
        func = c.get('func')
        name = c.get('name')
        app_name = func.__module__.split('.')[0]   
        prefix = apps_route_prefix.get(app_name)
        if prefix is None:
            prefix = ''
        url_path = parse.urljoin(prefix, url_path)
        if c.get('isregex'):
            p = re_path(url_path, func, name=name)
        else:
            p = path(url_path, func, name=name)
        if p.name not in get_objs_all_attr(url_patterns, "name"):
            url_patterns.append(p)

def delay_thread():
    time.sleep(0.5)
    set_path()

