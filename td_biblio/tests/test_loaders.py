# -*- coding: utf-8 -*-
"""
TailorDev Bibliography

Test loaders.
"""
from __future__ import unicode_literals

import datetime
import pytest

from django.test import TestCase
from eutils.exceptions import EutilsNCBIError

from ..utils.loaders import PubmedLoader
from ..models import Author, Entry, Journal


@pytest.mark.django_db
class PubmedLoaderTests(TestCase):
    """
    Tests for the pubmed loader
    """
    def setUp(self):
        """
        Set object level vars
        """
        self.PMID = 26588162
        self.loader = PubmedLoader()

    def test_load_records_with_an_existing_pmid(self):
        """Test single import given an existing PMID"""

        self.loader.load_records(PMIDs=self.PMID)

        self.assertEqual(len(self.loader.records), 1)

        record = self.loader.records[0]
        expected = {
            'title': (
                'Improved PEP-FOLD Approach for Peptide and Miniprotein '
                'Structure Prediction.'
            ),
            'authors': [
                {
                    'first_name': 'Y',
                    'last_name': 'Shen'
                },
                {
                    'first_name': 'J',
                    'last_name': 'Maupetit'
                },
                {
                    'first_name': 'P',
                    'last_name': 'Derreumaux'
                },
                {
                    'first_name': 'P',
                    'last_name': 'Tufféry'
                }
            ],
            'journal': 'J Chem Theory Comput',
            'volume': '10',
            'number': '10',
            'pages': '4745-58',
            'year': '2014',
            'publication_date': datetime.date(2014, 1, 1),
            'is_partial_publication_date': True
        }
        self.assertEqual(record['title'], expected['title'])
        self.assertEqual(record['authors'], expected['authors'])
        self.assertEqual(record['journal'], expected['journal'])
        self.assertEqual(record['volume'], expected['volume'])
        self.assertEqual(record['number'], expected['number'])
        self.assertEqual(record['pages'], expected['pages'])
        self.assertEqual(record['year'], expected['year'])
        self.assertEqual(
            record['publication_date'],
            expected['publication_date']
        )
        self.assertEqual(
            record['is_partial_publication_date'],
            expected['is_partial_publication_date']
        )

    def test_load_records_with_a_fake_string_as_pmid(self):
        """Test single import given a fake PMID"""

        with pytest.raises(EutilsNCBIError):
            self.loader.load_records(PMIDs='fakePMID')
        self.assertEqual(len(self.loader.records), 0)

    def test_save_records_with_an_existing_pmid(self):
        """Test single import given an existing PMID"""

        self.assertEqual(Author.objects.count(), 0)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(Journal.objects.count(), 0)

        self.loader.load_records(PMIDs=self.PMID)
        self.loader.save_records()

        self.assertEqual(Author.objects.count(), 4)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(Journal.objects.count(), 1)
