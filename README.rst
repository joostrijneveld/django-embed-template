django-embed-template |travis|
=====================

.. |travis| image:: https://travis-ci.org/joostrijneveld/django-embed-template.svg?branch=master
    :target: https://travis-ci.org/joostrijneveld/django-embed-template

This package adds the ``{% embed %}`` templatetag. This tag combines the functionality of `the include tag <https://docs.djangoproject.com/en/1.10/ref/templates/builtins/#include>`__ and `the extends tag <https://docs.djangoproject.com/en/1.10/ref/templates/builtins/#extends>`__ to allow for more flexible and extensible modular template usage. Inspired by `twig's embed tag <http://twig.sensiolabs.org/doc/tags/embed.html>`__, this tag lets you override blocks that were defined in the included template.

Requirements
------------

This package is tested with Django 1.8, 1.9 and 1.10 and their respectively supported Python versions.

Installation
------------

Simply get the package from ``pip``:

::

    pip install django-embed-template

Then make sure to add ``django_embed_template`` to your ``INSTALLED_APPS`` in your ``settings.py``.

Usage
-----

Unlike ``{% extends %}``, the ``{% embed %}`` tag can be repeated in the template and does not have to occur as the first tag (essentially like the ``{% include %}`` tag). Likewise, ``{% embed %}`` inherits the context by default, and allows you to pass additional context using the ``with`` keyword. Passing only the explicitly listed variables can be achieved using the ``only`` keyword.

In many cases ``{% include %}`` simply suffices. However, in more complex scenarios it has a tendency to create an exponential number of combined templates. This typically happens when the content of the included template is itself dynamic. Consider the following example (inspired by `twig's documentation <http://twig.sensiolabs.org/doc/tags/embed.html>`__):

Assume we have some ``base.html`` that contains a `content` block. In this block, we want to create vertical and horizontal sub-blocks. Assume we have ``vertical.html`` that contains two boxes sides by side with respectively ``{% block A %}`` and ``{% block B %}`` inside, as well as ``horizontal.html`` containing three stacked boxes with similarly labeled blocks. Our page could then look something like this:

::

    {% extends 'base.html' %}
    {% block content %}
        {% embed 'vertical.html' %}
            {% block A %}Arthur, King of the Britons{% endblock %}
            {% block B %}Sir Lancelot{% endblock %}
        {% endembed %}
        {% embed 'horizontal.html' %}
            {% block A %}Sir Bedevere the Wise{% endblock %}
            {% block B %}Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot{% endblock %}
            {% block C %}
                Other knights:
                {% embed 'horizontal.html' with background='gray' %}
                    {% block A %}Sir Galahad the Pure{% endblock %}
                    {% block B %}Sir Not Appearing In This Film{% endblock %}
                {% endembed %}
            {% endblock %}
        {% endembed %}
    {% endblock %}

Note that we're also nesting ``{% embed %}`` blocks, leaving some blocks unspecified, as well as passing context to one of the embedded templates. For more possible scenarios, browse through the `example templates <https://github.com/joostrijneveld/django-embed-template/tree/master/testprojects/common/templates>`__.

License
-------

This package includes code that was directly derived from code from the Django project. The included django-LICENSE applies to those snippets. The included CC0 license applies to the rest of this project.
