from django.conf import settings
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template import RequestContext


class BasicView(object):
    cache_key = None # Leave as none to disable context caching
    cache_time = 60*5 # 5 minutes
    content_type = settings.DEFAULT_CONTENT_TYPE
    file_attachment = False

    def __new__(cls, request, *args, **kwargs):
        instance = object.__new__(cls)
        if isinstance(instance, cls):
            instance.__init__(request, *args, **kwargs)
        return instance()

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        """Handle the request processing workflow."""
        return self.render()

    def get_cache_key(self):
        """Provide an opportunity to dynamically generate the cache key."""
        return self.cache_key

    def get_context(self):
        """
        Retrieve the cached context from the cache if it exists. Otherwise,
        generate it and cache it.
        """
        cache_key = self.get_cache_key()
        if cache_key is None:
            context_dict = self.cached_context()
        else:
            context_dict = cache.get(cache_key)
            if context_dict is None:
                context_dict = self.cached_context()
                cache.set(cache_key, context_dict, self.cache_time)
        context_dict.update(self.uncached_context())
        return context_dict

    def cached_context(self):
        """Provide the context that can be cached."""
        return {}

    def uncached_context(self):
        """Provide the context that should not be cached."""
        return {}

    def get_template(self):
        """
        Provide an opportunity for to dynamically generate the template name.
        """
        return self.template

    def render(self):
        """Take the context and render it using the template."""
        return render_to_response(self.get_template(), self.get_context(),
                                  RequestContext(self.request),
                                  mimetype=self.content_type)


class AjaxView(BasicView):
    """Returns a response containing the context serialized to Json"""
    content_type = 'application/json'

    def __call__(self):
        if not self.request.is_ajax():
            raise Http404
        return super(AjaxView, self).__call__()

    def render(self):
        json_data = simplejson.dumps(self.get_context(),
                                     cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type=self.content_type)


class FormView(BasicView):

    def __init__(self, request, *args, **kwargs):
        super(FormView, self).__init__(request, *args, **kwargs)
        self.data = getattr(self.request, 'POST', None)
        self.files = getattr(self.request, 'FILES', None)
        self.form_options = {}
        self.form = self.get_form()

    def __call__(self):
        if self.request.method == 'POST':
            response = self.process_form()
            # If a response was returned by the process_form method, then
            # return that response instead of the standard response.
            if response:
                return response

        return self.render()

    def uncached_context(self):
        """Add the form to the uncached context."""
        context = super(FormView, self).uncached_context()
        context.update({'form': self.form})
        return context

    def get_form(self):
        """
        Get the default form for the view, bound with data if provided.
        """
        if self.data:
            self.form_options.update({'data': self.data})
        if self.files:
            self.form_options.update({'files': self.files})
        return self.form_class(**self.form_options)

    def process_form(self):
        """
        The method to process POST requests. Return an HttpResponse when you
        need to circumvent normal view processing, such as redirecting to a
        success url.
        """
        if self.form.is_valid():
            self.form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Get the url to redirect to upon successful form submission."""
        return self.success_url


class MultiFormView(FormView):

    def __init__(self, request, *args, **kwargs):
        self.forms = {}
        super(MultiFormView, self).__init__(request, *args, **kwargs)

    def get_form(self):
        """
        Set self.forms to a dict of form_class keys to form instances, and
        return None for the value of self.form.
        """
        for form_name, form_class in self.form_classes.items():
            if not self.form_options.get(form_name):
                self.form_options[form_name] = {}
            if self.data:
                self.form_options[form_name].update({'data': self.data})
            if self.files:
                self.form_options[form_name].update({'files': self.files})
            self.forms[form_name] = \
                form_class(**self.form_options[form_name])
        return None

    def process_form(self):
        for form_name in self.form_classes.keys():
            if not self.forms[form_name].is_valid():
                # Return none so that the normal view processing will
                # continue, allowing the user to correct errors.
                return None

        # If all forms are valid, save them and redirect.
        for form_name in self.form_classes.keys():
            self.forms[form_name].save()
        return HttpResponseRedirect(self.get_success_url())

    def uncached_context(self):
        context = super(MultiFormView, self).uncached_context()
        for form_name in self.form_classes.keys():
            context.update({form_name: self.forms[form_name]})
        return context
