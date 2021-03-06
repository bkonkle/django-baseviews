Writing Views
=============

Basic Views
***********

The simplest views can be handled by creating a subclass of ``BasicView``,
defining the ``template`` attribute, and implementing the ``get_context``
method. ::
    
    from baseviews.views import BasicView
    from lol.models import Cheezburger
    
    class LolHome(BasicView):
        template = 'lol/home.html'
        
        def get_context(self):
            return {'burgers': Cheezburger.objects.i_can_has()}


Custom MIME type
****************

The MIME type defaults to the value of the ``DEFAULT_CONTENT_TYPE`` setting.
This can be overriden by defining the content_type attribute::
    
    from baseviews.views import BasicView
    from lol.models import Cheezburger
    
    class GoogleSiteMap(BasicView):
        template = 'sitemap.xml'
        content_type = 'application/xml'


Caching the Context
*******************

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
        
        def __init__(self, request, lol_slug):
            self.lol = Lol.objects.get(slug=lol_slug)
            super(LolDetail, self).__init__(request)
        
        def get_cache_key(self):
            return self.cache_key % self.lol.slug


Ajax Views
**********

The ``AjaxView`` class is a subclass of ``BasicView`` that takes the context
and uses simplejson to dump it to a JSON object.  If the view is not requested
via Ajax, it raises an Http404 exception.


Decorators
**********

Built-in decorators such as login_required don't work by default with
class-based views.  This is because the first argument passed to the decorator
is the class instance, not the request object.

To decorate a class-based view, simply use the helper
``django.utils.decorators.method_decorator`` on the ``__new__`` method like
this::

    from django.utils.decorators import method_decorator
    from django.contrib.auth.decorators import login_required
    from baseviews.views import BasicView
    
    class BucketFinder(BasicView):
        template = 'lol/wheres_mah_bucket.html'
        
        @method_decorator(login_required)
        def __new__(cls, *args, **kwargs):
            return super(BucketFinder, cls).__new__(cls, *args, **kwargs)


Form Views
**********

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
        template = 'lol/kitteh.html'
        form_class = KittehForm
        
        def __init__(self, request, kitteh_slug):
            self.kitteh = get_object_or_404(Kitteh, slug=kitteh_slug)
            super(KittehView, self).__init__(request)
        
        def get_form(self):
            self.form_options = {'request': self.request,
                                 'kitteh': self.kitteh}
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


Views with Multiple Forms
*************************

If you need multiple forms in one view, use MultiFormView.  This is a subclass
of FormView that allows you to provide ``form_classes`` dict as an attribute
on the class, mapping form names to form classes.  The form names will be
used as the keys to form instances, and each form name will be turned into
a context variable providing the form instances to your template.

::

    class MonorailCatTicketsView(MultiFormView):
        template = 'lol/monorail_tickets.html'
        form_classes = {'kitteh_form': KittehForm,
                        'payment_form': PaymentForm}
        
        def __init__(self, request, kitteh_slug):
            self.kitteh = get_object_or_404(Kitteh, slug=kitteh_slug)
            super(MonorailCatTicketsView, self).__init__(request)
        
        def get_form(self):
            self.form_options['kitteh_form'] = {'request': self.request,
                                                'kitteh': self.kitteh}
            self.form_options['payment_form'] = {'user': self.request.user}
            return super(MonorailCatTicketsView, self).get_form()
        
        def get_success_url(self):
            return reverse('monorail_cat_thanks_you', args=[self.kitteh.slug])


Mapping the Views to URLs
*************************

In order to make the use of class attributes safe, baseviews overrides the
``__new__`` method on the class.  This means that you can simply map the url
pattern directly to the class::

    from lol import views
    
    urlpatterns = patterns('',
        url(r'^$', views.LolHome, name='lol_home'),
    )
