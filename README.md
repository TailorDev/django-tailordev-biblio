TailorDev Biblio
================

Scientific bibliography management with Django.

## Dependencies

For now, Django>=1.5 is required for this project to run on production, with python>=2.6.

## Installation

The easiest way to go is to use pip:

    $ pip install django-tailordev-biblio

If you intend to work on the code, clone this repository and install all dependencies at once via:

    $ pip install -r requirements/local.txt

And then install the package in development mode:

    $ python setup.py develop

## Configuration

Add `td_biblio` to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
    ...
        'td_biblio',
    ...
    )

Add `td_biblio` urls to your project url patterns:

    urlpatterns = patterns('',
        ...
        url(r'^bibliography/', include('td_biblio.urls')),
        ...
    )

And then update your database:

    $ python manage.py syncdb

## Templates

Create a base template to inherit from. It should be visible as `_layouts/base.html`

## Import BibTex bibliography

Once `td_biblio` is fully functional, you may want to import your references via:

    $ python manage.py bibtex_import my_bibliography.bib

## Running the Tests

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
