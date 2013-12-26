# -*- coding: utf-8 -*-
import os

from pip.req import parse_requirements
from setuptools import setup, find_packages


REQUIREMENTS = 'requirements.txt'


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_dependencies(requirements):
    """Return project dependencies as read from the requirements file"""
    r = parse_requirements(requirements)
    return [str(d.req) for d in r]


setup(
    name='django-tailordev-biblio',
    version=__import__('td_biblio').__version__,
    author='Julien Maupetit',
    author_email='julien@tailordev.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://bitbucket.org/tailordev/django-tailordev-biblio',
    license='MIT',
    description=u' '.join(__import__('td_biblio').__doc__.splitlines()).strip(),  # NOPEP8
    long_description=read_file('README.md'),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    install_requires=get_dependencies(REQUIREMENTS),
    test_suite="runtests.runtests",
    zip_safe=False,
)
