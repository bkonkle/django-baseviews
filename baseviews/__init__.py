from views import *


def view_factory(view_class, *args, **kwargs):
    """
    Thread-safe view class creator that instantiates view classes on demand
    so that attributes can safely be used.
    """
    def view(request, *vargs, **vkwargs):
        return view_class(*args, **kwargs)(request, *vargs, **vkwargs)
    return view

def decorate(function_decorator):
    """
    A decorator to allow the use of decorators that were created for
    function-based views.  It calls the decorator without the 'self' argument,
    and then takes the function that the decorator returns and calls it with
    the 'self' argument included.
    """
    def decorate_method(unbound_method):
        def method_proxy(self, *args, **kwargs):
            def f(*a, **kw):
                return unbound_method(self, *a, **kw)
            return function_decorator(f)(*args, **kwargs)
        return method_proxy
    return decorate_method