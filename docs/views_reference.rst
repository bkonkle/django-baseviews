View Reference
==============

This document describes the details of the view classes that baseviews
provides.

BasicView
*********

.. class:: BasicView
    
    A basic view that renders context to template, optionally caching the
    context.
    
    .. attribute:: cache_key
    
        Set this to a string to enable caching.  An easy way to use a dynamic
        cache key is to include string formatting specifiers in the string,
        which you can then convert in the ``get_cache_key`` method.
    
    .. attribute:: cache_time
    
        Controls the time, in seconds, to use for in caching.  It defaults to
        the arbitrary value of 5 minutes.
    
    .. attribute:: content_type
    
        Provides an opportunity to customize the mimetype used in the
        ``render`` method.  Defaults to ``settings.DEFAULT_CONTENT_TYPE``.

    .. method:: get_context()
    
        This returns the context that is passed to the ``render``
        method.  Override this method to provide context to your template.
    
    .. method:: cached_context()
    
        If ``get_context`` is not overridden, it will call this method to
        retrieve the context.  If the ``cache_key`` attribute on the view
        class is set, then it will cache this context.
    
    .. method:: uncached_context()
    
        After it retrieves ``cached_context``, the ``get_context`` method
        calls this and updates the context dict with the context this method
        returns.  The context will not be cached.
    
    .. method:: get_cache_key()
    
        By default, this simply returns the ``cache_key`` attribute from the
        view class.  The point of this is to give you a chance to dynamically
        generate the cache key based on the request, including things like
        object id's or slugs in the key that is returned by this method.
    
    .. method:: get_template()
    
        This defaults to the ``template`` attribute, but the method can be
        overridden in order to dynamically generate the template based on the
        request.
    
    .. method:: render()
    
        Calls ``get_template`` and ``get_context``, and renders the template
        with the mimetype from the ``content_type`` attribute.  This can be
        overridden to customize the rendering, such as outputting to different
        formats like JSON.
    
    .. method:: __init__()

        Sets the request, args, and kwargs as attributes on the class
        instance.

    .. method:: __call__()

        Returns the results of ``render``.


AjaxView
********

.. class:: AjaxView

    A subclass of :class:`BasicView` that returns the context rendered to a
    JSON object.

    .. attribute:: content_type
    
        This defaults to *"application/json"*.
    
    .. method:: __call__()
    
        Checks to make sure that the request is Ajax-based.  If not, raises a
        404.
    
    .. method:: render()
    
        Uses simplejson to render the context as a JSON object.
