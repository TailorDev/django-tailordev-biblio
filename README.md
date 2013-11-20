TailorDev Biblio
================

A scientific bibliography management reusable django application.

## Dependencies

For now, Django>=1.5 is required for this project to run on production, with python>=2.6. Currently, this application is not compatible with python 3.3. We are working on it.

## Installation

To install all dependencies at once, use pip:

    $ pip install -r requirements.txt

If you intend to test or improve this application, also install the local dependencies:

    $ pip install -r requirements/local.txt

Add `td_biblio` and its dependencies to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
    ...
        'td_biblio',
    ...
    )

Add `td_biblio` urls to your project url patterns:

    urlpatterns = patterns('',
        ...
        url(r'^mypattern/', include('td_biblio.urls')),
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
