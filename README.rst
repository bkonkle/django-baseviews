Django-Baseviews
================

A small collection of base view classes to build upon. They are intended to
handle a lot of the repetition in common view patterns and allow you to focus
on what makes each view different.

This is just the beginning, and I plan on expanding these classes and adding
more to cover other common view patterns.  Feel free to fork and send pull
requests - I'd be happy to review and integrate contributions.

Installation
************

Use pip to install the module::

    $ pip install django-baseviews

Then simply import it for use in your views::

    import baseviews

Writing Views
*************

Basic Views
-----------


The simplest views can be handled by creating a subclass of ``BasicView``,
defining the ``template`` attribute, and implementing the ``get_context``
method. ::
    
    from baseviews import BasicView
    from lol.models import Cheezburger
    
    class LolHome(BasicView):
        template = 'lol/home.html'
        
        def get_context(self):
            return {'burgers': Cheezburger.objects.i_can_has()}

Custom MIME type
----------------

As with Django itself, the MIME type defaults to the value of the ``DEFAULT_CONTENT_TYPE`` setting. This can be overriden by defining the content_type attribute. ::
    
    from baseviews import BasicView
    from lol.models import Cheezburger
    
    class GoogleSiteMap(BasicView):
        template = 'sitemap.xml'
        content_type = 'application/xml'

Caching the Context
-------------------

If you'd like to cache the context through the low-level cache API, add the
``cache_key`` and ``cache_time`` attributes and override the
``cached_context`` method instead of the ``get_context`` method.
Additionally, you can override ``uncached_context`` to add context that
shouldn't be cached.  If ``cache_time`` isn't set, it defaults to the
arbitrary length of 5 minutes. ::
    
    class LolHome(BasicView):
        template = 'lol/home.html'
        cache_key = 'lol_home'
        cache_time = 60*20 # 20 minutes
    
        def cached_context(self):
            return {'burgers': Cheezburger.objects.i_can_has()}

The ``cache_key`` attribute can include string formatting, which you can
populate by overriding the ``get_cache_key`` method::

    class LolDetail(BasicView):
        template = 'lol/detail.html'
        cache_key = 'lol_detail:%s'
        cache_time = 60*20 # 20 minutes
        
        def __call__(self, request, lol_slug):
            self.lol = Lol.objects.get(slug=lol_slug)
            return super(LolDetail, self).__call__(self, request)
        
        def get_cache_key(self):
            return self.cache_key % self.lol.slug

Ajax Views
----------

The ``AjaxView`` class is a subclass of ``BasicView`` that takes the context
and uses simplejson to dump it to a JSON object.  If the view is not requested
via Ajax, it raises an Http404 exception.

Decorators
----------

Built-in decorators such as login_required don't work by default with
class-based views.  This is because the first argument passed to the decorator
is the class instance, not the request object.  Todd Reed posted an excellent
solution to this problem on
`his blog <http://www.toddreed.name/content/django-view-class/>`__.

I've added his solution to ``baseviews`` as ``decorate``.  To decorate a
class-view method, use ``decorate`` like this::

    from django.contrib.auth.decorators import login_required
    from baseviews import decorate, BasicView
    
    class BucketFinder(BasicView):
        template = 'lol/wheres_mah_bucket.html'
        
        @decorate(login_required)
        def __call__(self, request):
            return super(BucketFinder, self).__call__(request)

Form Views
----------

Form processing can be simplified with a subclass of the ``FormView`` class.
Define an extra attribute called ``form_class`` and set it to the form you'd
like to use, and define an attribute called ``success_url`` with the name of
the url to be redirected to after successful form processing.  You can also
override the ``get_success_url`` method to provide a dynamic success url.

The most basic processing can be handled without any further effort.
``FormView`` will get the form and add it to the context, and if the request
method is POST it will attempt to validate and save it.

If you would like to do more, you can extend the ``get_form`` and
``process_form`` methods::

    class KittehView(FormView):
        form_class = KittehForm
        
        def __call__(self, request, kitteh_slug):
            self.kitteh = get_object_or_404(Kitteh, slug=kitteh_slug)
            return super(KittehView, self).__call__(request)
        
        def get_form(self):
            self.form_options = {'request': self.request, 'kitteh': self.kitteh}
            return super(KittehView, self).get_form()
        
        def process_form(self):
            if self.request.POST.get('edit', False):
                if self.form.is_valid():
                    self.form.save()
                    return redirect(self.get_success_url())
            elif self.request.POST.get('delete', False):
                self.kitteh.delete()
                return redirect('kitteh_deleted')
        
        def get_success_url(self):
            return reverse('kitteh_edited', args=[self.kitteh.slug])

Mapping the Views to URLs
*************************

In order to make the use of class attributes safe, views need to be mapped to
urls using a view factory.  The one in ``baseviews`` is borrowed from
``django-haystack``. ::

    from baseviews import view_factory
    from lol import views
    
    urlpatterns = patterns('',
        url(r'^$', view_factory(views.LolHome), name='lol_home'),
    )
