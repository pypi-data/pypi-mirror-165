Add `django_moo_url` in you `INSTALL_APPS`.

## Quick Start

**step1**.  Add `autodiscover_modles` in your `apps.py` so that sure your `views.py` could conduct successfully.

```python
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self) -> None:
        autodiscover_modules("views.py")
```

**step 2**. use the decorator in function view.

```python
from django.http import JsonResponse
from django_moo_url import url_pattern

@url_pattern("index/")
def index(request):
    return JsonResponse({"hello":"world"})
```

use the decorator in class view.

```python
from django.http import JsonResponse
from django_moo_url import url_pattern
from django.views import View

class IndexView(View):
    @url_pattern("index/")
    def get(request):
        return JsonResponse({"hello":"world"})
```

OK, you learn how to use this library in your `django` project. now, let us learn some more challenge thing.

## Other Function

### Add prefix

Add next code in your `settings.py` like this:

```python
DJANGO_URL = {
    'myapp': "api/v1/pub"
}
```

so, you could visit http://localhost:8000/api/v1/pub/index to get your interface you write.

### About `url_pattern` 

It could get three arguments:

- `url_path`: required,url path you like.
- `is_regex`: `False` , if it's `True`, it will use `re_path` to add router.
- `name`: like `path` and `re_path` argument, if you don't provide, it will use your function name.

