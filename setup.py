#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


REQUIREMENTS = 'requirements/production.txt'

with open('README.md') as f:
    readme = f.read()


def parse_requirements(requirements, ignore=('setuptools',)):
    """Read dependencies from requirements file (with version numbers if any)

    Note: this implementation does not support requirements files with extra
    requirements
    """
    with open(requirements) as f:
        packages = set()
        for line in f:
            line = line.strip()
            if line.startswith(('#', '-r', '--')):
                continue
            if '#egg=' in line:
                line = line.split('#egg=')[1]
            pkg = line.strip()
            if pkg not in ignore:
                packages.add(pkg)
        return packages

setup(
    name='django-tailordev-biblio',
    version=__import__('td_biblio').__version__,
    author='Julien Maupetit',
    author_email='julien@tailordev.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://bitbucket.org/tailordev/django-tailordev-biblio',
    license='MIT',
    description=' '.join(__import__('td_biblio').__doc__.splitlines()).strip(),  # noqa
    long_description=readme,
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
    ],
    install_requires=parse_requirements(REQUIREMENTS),
    test_suite='runtests.runtests',
    zip_safe=False,
)
