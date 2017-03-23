# Django TailorDev Biblio

Bibliography management with Django.

[![](https://travis-ci.org/TailorDev/django-tailordev-biblio.svg?branch=master)
](https://travis-ci.org/TailorDev/django-tailordev-biblio/)
[![](https://img.shields.io/pypi/v/django-tailordev-biblio.svg)](https://pypi.python.org/pypi/django-tailordev-biblio)

## Compatibility

Since the `1.0.0` release, we have added full support for recent python and
Django releases:

|            | Django 1.7         | Django 1.8         | Django 1.9         | Django 1.10        |
| --         | --                 | --                 | --                 | --                 |
| Python 2.7 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Python 3.4 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Python 3.5 |                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Python 3.6 |                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

Please note that for older Python and/or Django versions, you can still use the `0.3` release.

## Installation

### Install `td_biblio`

The easiest way to go is to use pip:

```bash
$ pip install -U django-tailordev-biblio
```

### Configure `td_biblio`

Add `td_biblio` to your `INSTALLED_APPS` in django settings:

```python
# foo_project/settings.py

INSTALLED_APPS = (
    # other apps…
    'td_biblio',
)
```

Add `td_biblio` urls your project url patterns:

```python
# foo_project/urls.py

urlpatterns = [
    # other urls…
    url(r'^bibliography/', include('td_biblio.urls')),
]
```

And finally migrate your database from your project root path:

```bash
$ python manage.py migrate td_biblio
```

### Add a base template

In order to use `td_biblio` templates, you will need to create a base template
to inherit from. This base template should be visible as `_layouts/base.html`
and contains at least the following blocks:

```html
<html>
  <head>
    <title>Publication list</title>
  </head>
  <body>
    {% block content %}{% endblock content %}
    {% block javascripts %}{% endblock javascripts %}
  </body>
</html>
```

As you might have guessed, the `content` block is the base block where we render
the bibliography list and item details, while the `javascripts` block contains
eponym front-end dependencies. You will find an example base layout template at:
[`td_biblio/templates/_layouts/base.html`](https://github.com/TailorDev/django-tailordev-biblio/blob/master/td_biblio/templates/_layouts/base.html)

## Import BibTex bibliography

Once `td_biblio` is installed and configured, you may want to import your
references stored in a BibTeX file. Hopefully, there is a command for that:

```bash
$ python manage.py bibtex_import my_bibliography.bib
```

## Hack

### Development installation

If you intend to work on the code, clone this repository and install all
dependencies in a virtual environment:

```bash
$ python -m venv venv  # create a virtualenv
$ source venv/bin/activate  # activate this virtualenv
(venv) $ pip install -r requirements-dev.txt
```

And then install the package in development mode:

```bash
(venv) $ python setup.py develop
```

### Running the Tests

You can run the tests with via:

```bash
(venv) $ py.test
```

## License

`django-tailordev-biblio` is released under the MIT License. See the bundled
LICENSE file for details.
