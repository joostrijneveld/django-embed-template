django-embed-template
=====================

This package adds the ``{% embed %}`` templatetag. This tag combines the functionality of `the include tag <https://docs.djangoproject.com/en/1.9/ref/templates/builtins/#include>`__ and `the extends tag <https://docs.djangoproject.com/en/1.9/ref/templates/builtins/#extends>`__ to allow for more flexible and extensible modular template usage. Inspired by `twig's embed tag <http://twig.sensiolabs.org/doc/tags/embed.html>`__, this tag lets you override blocks that were defined in the included template.

Installation
------------

Simply get the package from ``pip``:

::

    pip install django-embed-template

Then make sure to add ``django_embed_template`` to your ``INSTALLED_APPS`` in your ``settings.py``.

Usage
-----

Unlike ``{% extends %}``, the ``{% embed %}`` tag can be repeated in the template and does not have to occur as the first tag (essentially like the ``{% include %}`` tag). Likewise, ``{% embed %}`` inherits the context by default, and allows you to pass additional context using the ``with`` keyword. Passing only the explicitly listed variables can be achieved using the ``only`` keyword.

*TODO add an example*

License
-------

This package includes code that was directly derived from code from the Django project. The included django-LICENSE applies to those snippets. The included CC0 license applies to the rest of this project.
