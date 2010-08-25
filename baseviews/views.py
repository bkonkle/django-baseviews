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
    
    def __call__(self, request):
        """Handle the request processing workflow."""
        self.request = request
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
        context_dict = not cache_key is None and cache.get(cache_key)
        if context_dict is None:
            context_dict = self.cached_context()
            if not cache_key is None:
                cache.set(cache_key, context_dict, self.cache_time)
        context_dict.update(
            self.uncached_context()
        )
        return context_dict
    context = property(get_context)
    
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
        return render_to_response(self.get_template(), self.context,
                                  RequestContext(self.request))

class AjaxView(BasicView):
    """Returns a response containing the context serialized to Json"""
    def __call__(self, request):
        if not request.is_ajax():
            raise Http404
        return super(AjaxView, self).__call__(request)
    
    def render(self):
        json_data = simplejson.dumps(self.context, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type='application/json')

class FormView(BasicView):
    
    def __call__(self, request):
        self.request = request
        self.form_options = {}
        self.form = self.get_form()
        
        if request.method == 'POST':
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
    
    def process_form(self):
        """
        The method to process POST requests. Return an HttpResponse when you
        need to circumvent normal view processing, such as redirecting to a
        success url.
        """
        if self.form.is_valid():
            self.form.save()
            return HttpResponseRedirect(
                self.get_success_url()
            )

    def get_form(self):
        """
        Get the default form for the view, bound with data if provided.
        """
        data = getattr(self.request, 'POST', None)
        if data:
            self.form_options.update({'data': data})
        return self.form_class(**self.form_options)
    
    def get_success_url(self):
        """Get the url to redirect to upon successful form submission."""
        return self.success_url

