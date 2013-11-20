{{ app_name }}
========================

Welcome to the documentation for django-{{ app_name }}!

## Dependencies

CHANGE ME

## Installation

To install all dependencies at once, use pip:

    $ pip install -r requirements.txt

If you intend to test or improve this application, also install the local dependencies:

    $ pip install -r requirements/local.txt

Add `{{ app_name }}` and its dependencies to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
    ...
        '{{ app_name }}',
    ...
    )


Add `{{ app_name }}` urls to your project url patterns:

    urlpatterns = patterns('',
        ...
        url(r'^mypattern/', include('{{ app_name }}.urls')),
        ...
    )

And then update your database:

    $ python manage.py syncdb
    $ python manage.py migrate

## Templates

Create a base template to inherit from. It should be visible as `_layouts/base.html`

## Running the Tests

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
