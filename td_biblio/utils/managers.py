# -*- coding: utf-8 -*-
"""
Bibliography Manager Tools
"""
import datetime
import logging

import bibtexparser

from bibtexparser import customization as bp_customization
from bibtexparser.bparser import BibTexParser
from bibtexparser.latexenc import string_to_latex
from time import strptime

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


def bibtex_import(bibtex_filename):
    """
    Import a bibtex (.bib) bibliography file
    """
    logger.info("BibTex import: %s" % bibtex_filename)
    simple_fields = ('type', 'title', 'volume', 'number', 'pages', 'url')
    date_fields = ('day', 'month', 'year')

    with open(bibtex_filename) as bibtex_file:

        # Parse BibTex file
        parser = BibTexParser()
        parser.customization = td_biblio_customization
        bp = bibtexparser.load(bibtex_file, parser=parser)

        # Import each entry
        for bib_item in bp.get_entry_list():

            logger.debug("BibTex entry: %s", bib_item)

            # Simple fields
            fields = dict(
                (k, v) for (k, v) in bib_item.items() if k in simple_fields
            )

            # Publication date
            publication_date = {'day': 1, 'month': 1, 'year': 1900}
            item_date = dict(
                (k, v) for (k, v) in bib_item.items() if k in date_fields
            )
            publication_date.update(item_date)
            # Check if month is numerical or not
            month = publication_date['month']
            try:
                int(month)
            except:
                publication_date['month'] = strptime(month, '%b').tm_mon
            # Convert date fields to integers
            publication_date = dict(
                (k, int(v)) for k, v in publication_date.items()
            )
            fields['publication_date'] = datetime.date(**publication_date)

            fields['is_partial_publication_date'] = not all(
                [True if k in item_date else False for k in date_fields]
            )

            # Foreign keys
            journal, _ = Journal.objects.get_or_create(
                name=bib_item['journal']
            )
            fields['journal'] = journal

            logger.debug("Fields: %s", fields)

            # Save or Update this entry
            entry, _ = Entry.objects.get_or_create(**fields)
            logger.debug("Entry: %s", entry)

            # Authors
            for rank, author in enumerate(bib_item['author']):
                splited = author.split(', ')
                last_name = splited[0]
                first_name = " ".join(splited[1:])

                author, _ = Author.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name)

                AuthorEntryRank.objects.get_or_create(
                    entry=entry,
                    author=author,
                    rank=rank)

    logger.info("Importation done.")
