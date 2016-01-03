from functools import partial
import django.contrib.auth.decorators as decorators


permission_required = partial(decorators.permission_required,
                              login_url=None,
                              raise_exception=True)
