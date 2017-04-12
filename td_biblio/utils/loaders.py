# -*- coding: utf-8 -*-
"""
Bibliography Manager Tools
"""
from __future__ import unicode_literals

import datetime
import logging

import bibtexparser
import eutils.client

from time import strptime

from bibtexparser import customization as bp_customization
from bibtexparser.bparser import BibTexParser
from bibtexparser.latexenc import string_to_latex
from django.utils.translation import ugettext_lazy as _

from ..models import Author, Journal, Entry, AuthorEntryRank


logger = logging.getLogger('td_biblio')


def to_latex(record):
    """
    Convert strings to latex
    """
    for val in record:
        record[val] = string_to_latex(record[val])
    return record


def td_biblio_customization(record):
    """
    Customize BibTex records parsing
    """
    # Convert crapy things to latex
    record = to_latex(record)
    # and then to unicode
    record = bp_customization.convert_to_unicode(record)
    record = bp_customization.type(record)
    record = bp_customization.author(record)
    record = bp_customization.editor(record)
    record = bp_customization.page_double_hyphen(record)

    return record


class BaseLoader(object):

    def __init__(self):
        self.entry_base_fields = (
            'type', 'title', 'volume', 'number', 'pages', 'url',
            'publication_date', 'is_partial_publication_date'
        )
        self.records = []

    def to_record(self, input):
        """Convert an item to import to a valid record

        valid_record = {
            'title': 'A coarse-grained protein force field …',
            'authors': [
                {
                    'first_name': 'Julien',
                    'last_name': 'Maupetit'
                },
                {
                    'first_name': 'P',
                    'last_name': 'Tuffery'
                },
                {
                    'first_name': 'Philippe',
                    'last_name': 'Derreumaux'
                }
            ],
            'journal': 'Proteins: Structure, Function, and Bioinformatics',
            'volume': '69',
            'number': '2',
            'pages': '394--408',
            'year': '2007',
            'publisher': 'Wiley Online Library',
            'ENTRYTYPE': 'article',
            'ID': 'maupetit2007coarse',
            'publication_date': datetime.date(2007, 1, 1),
            'is_partial_publication_date': True
        }
        """
        raise NotImplemented(
            _(
                "You should implement a to_record method for {}".format(
                    self.__class__.__name__
                )
            )
        )

    def load_records(self, **kwargs):
        """Load all records in self.records"""

        raise NotImplemented(
            _(
                "You should implement a load_records method for {}".format(
                    self.__class__.__name__
                )
            )
        )

    def save_record(self, record):
        """Save a single record"""

        logger.debug("Record: {}".format(record))

        entry_fields = dict(
            (k, v) for (k, v) in record.items() if k in self.entry_base_fields
        )

        # Foreign keys
        journal, is_new = Journal.objects.get_or_create(
            name=record['journal']
        )
        entry_fields['journal'] = journal
        logger.debug("Journal: {}".format(journal))

        # Save or Update this entry
        entry, is_new = Entry.objects.get_or_create(**entry_fields)

        # Authors
        for rank, record_author in enumerate(record['authors']):
            author, _ = Author.objects.get_or_create(
                first_name=record_author['first_name'],
                last_name=record_author['last_name'],
            )

            AuthorEntryRank.objects.get_or_create(
                entry=entry,
                author=author,
                rank=rank,
            )
        logger.debug("(New) Entry imported with success: {}".format(entry))

    def save_records(self):
        """Batch save records"""
        for record in self.records:
            self.save_record(record)


class BibTeXLoader(BaseLoader):
    """BibTeXLoader

    This loader is designed to import a bibtex file items.

    Usage:

    >>> from td_biblio.utils.managers import BibTeXLoader
    >>> loader = BibTeXLoader()
    >>> loader.load_records(bibtex_filename='foo.bib')
    >>> loader.save_records()
    """

    def to_record(self, input):
        """Convert a bibtex item to a valid record"""

        # Simple fields
        record = input.copy()

        # Journal
        record['journal'] = input['journal']

        # Publication date
        pub_date = {'day': 1, 'month': 1, 'year': 1900}
        input_date = dict(
            (k, v) for (k, v) in input.items() if k in pub_date.keys()
        )
        pub_date.update(input_date)
        # Check if month is numerical or not
        try:
            int(pub_date['month'])
        except:
            pub_date['month'] = strptime(pub_date['month'], '%b').tm_mon
        # Convert date fields to integers
        pub_date = dict(
            (k, int(v)) for k, v in pub_date.items()
        )
        record['publication_date'] = datetime.date(**pub_date)

        record['is_partial_publication_date'] = not all(
            [True if k in input else False for k in pub_date.keys()]
        )

        # Authors
        record['authors'] = []
        for author in input['author']:
            splited = author.split(', ')
            record['authors'].append(
                {
                    'first_name': " ".join(splited[1:]),
                    'last_name': splited[0],
                }
            )
        return record

    def load_records(self, bibtex_filename=None):
        """Load all bibtex items as valid records"""

        with open(bibtex_filename) as bibtex_file:
            # Parse BibTex file
            parser = BibTexParser()
            parser.customization = td_biblio_customization
            bp = bibtexparser.load(bibtex_file, parser=parser)
            self.records = [self.to_record(r) for r in bp.get_entry_list()]


class PubmedLoader(BaseLoader):
    """PubmedLoader

    This loader is designed to fetch & import a list of Pubmed IDs

    Usage:

    >>> from td_biblio.utils.managers import PubmedLoader
    >>> loader = PubmedLoader()
    >>> loader.load_records(PMIDs=26588162)
    >>> loader.save_records()
    """

    def __init__(self, *args, **kwargs):
        super(PubmedLoader, self).__init__(*args, **kwargs)
        self.client = eutils.client.Client()

    def to_record(self, input):
        """Convert eutils PubmedArticle xml facade to a valid record"""

        record = {
            'title': input.title,
            'authors': [],
            'journal': input.jrnl,
            'volume': input.volume,
            'number': input.issue,
            'pages': input.pages,
            'year': input.year,
            'publication_date': datetime.date(int(input.year), 1, 1),
            'is_partial_publication_date': True
        }

        for author in input.authors:
            splited = author.split()
            record['authors'].append(
                {
                    'first_name': " ".join(splited[1:]),
                    'last_name': splited[0],
                }
            )

        return record

    def load_records(self, PMIDs=None):
        """Load all PMIDs as valid records"""

        entries = self.client.efetch(db='pubmed', id=PMIDs)
        self.records = [self.to_record(r) for r in entries]
