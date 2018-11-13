# TailorDev Biblio

## 2.0.0 (November 13, 2018)

- Add Django 2+ compatibility
- Add authors duplication cleanup form (#22)

### BC Breaks

- Drops compatibility with Django 1.7

## 1.2.0 (December 1, 2017)

- Make PMIDLoader & DOILoader bullet-proof

## 1.1.0 (June 14, 2017)

- Add PMIDLoader & DOILoader
- Add references importation view for admins (from PMIDs or DOIs)
- Better integrate the sandbox
- Make the sandbox deployable to Heroku

## 1.0.0 (March 23, 2017)

- Add support for python 3.4+
- Add support for Django 1.7+
- Switch to `py.test` test runner
- Remove jQuery implicit dependency

### BC Breaks

- Drops compatibility with python 2.6
- Drops compatibility with Django < 1.7

### 1.0.1 (March 23, 2017)

- Fix missing dev requirments

## 0.3 (February 3, 2015)

- Add publication list partial template

## 0.2 (June 2, 2014)

- Add support for partial publication date

### 0.2.1 (February 3, 2015)

- Entry first and last author are now object properties

## 0.1 (January 10, 2014)

First public release. Main features are:

- basic bibliography management
- bibtex file import
- django users/authors linking
- reference list view filtering by author, date, collections

TODO:

- Work on the documentation
- Add EndNote support
