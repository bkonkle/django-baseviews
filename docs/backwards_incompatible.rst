.. _backwards_incompatible:

Backwards-Incompatible Changes
==============================

Version 0.5
***********

* **Removed the "from views import *" call from "__init__"** - This was
  there to provide backwards compatibility for when baseviews was a single
  file instead of a package. This is not a good practice in general,
  and it caused problems when trying to implement formal versioning. All
  instances of ``from baseviews import`` in your code will need to be replaced
  with ``from baseviews.views import``.


Version 0.4
***********

* **"view_factory" removed** - With the addition of the ``__new__`` method
  override, the class can now used in the url mapping directly.  This
  eliminates the need for a view factory.

* **View args and kwargs handled in "__init__"** - Previously, the view
  arguments such as ``request`` and args and kwargs from the url pattern were
  handled by the ``__call__`` method.  Now, they are (more appropriately)
  handled by the ``__init__`` method and the ``__call__`` method is called
  without any additional arguments.  You'll need to adjust your subclasses
  accordingly.

* **"decorate" removed** - Jannis Leidel pointed out that Django has an
  equivalent method decorator built in, at
  ``django.utils.decorators.method_decorator``.  This eliminates the need for
  a custom ``decorate`` decorator.
