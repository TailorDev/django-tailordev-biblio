#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


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
    author='TailorDev',
    author_email='hello+github@tailordev.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/TailorDev/django-tailordev-biblio',
    license='MIT',
    description=' '.join(__import__('td_biblio').__doc__.splitlines()).strip(),  # noqa
    long_description=readme,
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
    ],
    install_requires=parse_requirements('requirements/base.txt'),
    tests_require=parse_requirements('requirements/dev.txt'),
    keywords='django biblio bibliography bibtex publication',
)
