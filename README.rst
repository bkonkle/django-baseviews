Django-Baseviews
================

A small collection of base view classes to build upon. They are intended to
handle a lot of the repetition in common view patterns and allow you to focus
on what makes each view different. They were created by Brandon Konkle, and
are used on some of the newer views at the Pegasus News and Daily You sites.

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
    
    from baseviews import BaseView
    from lol.models import Cheezburger
    
    class LolHome(BasicView):
        template = 'lol/home.html'
        
        def get_context(self):
            return {'burgers': Cheezburger.objects.i_can_has()}

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

Form Views
----------

Form processing can be simplified with a subclass of the ``FormView`` class.
Define an extra attribute called ``form_class`` and set it to the form you'd
like to use.  The most basic processing can be handled without any further
effort.  ``FormView`` will get the form and add it to the context, and if the
request method is POST it will attempt to validate and save it.

If you would like to do more, you can extend the ``get_form`` and
``process_form`` methods::

    def get_form(self):
        self.form_options = {'request': self.request, 'kitteh': self.kitteh}
        return super(KittehView, self).get_form()
    
    def process_form(self):
        if self.request.POST.get('edit', False):
            if self.form.is_valid():
                self.form.save()
                return redirect('kitteh_edited',
                                slug=self.kitteh.slug)
        elif self.request.POST.get('delete', False):
            self.kitteh.delete()
            return redirect('kitteh_deleted')

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
