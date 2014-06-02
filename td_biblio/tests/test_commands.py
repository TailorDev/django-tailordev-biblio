# -*- coding: utf-8 -*-
"""
TailorDev Bibliography

Test commands.
"""
import os.path

from django.core.management.base import CommandError
from django.test import TestCase

from ..management.commands import bibtex_import
from ..models import Author, Entry, Journal


class BibTexImportCommandTests(TestCase):
    """
    Tests for the bibtex_import admin command
    """
    def setUp(self):
        """
        Set object level vars
        """
        self.bibtex_file = os.path.abspath(
            os.path.dirname(__file__) + "/fixtures/biblio.bib"
        )
        self.cmd = bibtex_import.Command()

    def test_command(self):
        """
        Test python manage.py bibtex_import biblio.bib
        """
        # Without an input file to handle, cmd shoud assert a CommandError
        with self.assertRaises(CommandError):
            self.cmd.handle()

        # Execute the command
        self.cmd.handle(self.bibtex_file)

        # How many entries did we successfully import?
        self.assertEqual(Entry.objects.count(), 9)

        # How many journals?
        self.assertEqual(Journal.objects.count(), 5)

        # How many authors?
        self.assertEqual(Author.objects.count(), 31)

    def _test_entry_authors(self, entry, expected_authors):
        for rank, author in enumerate(entry.get_authors()):
            self.assertEqual(
                unicode(author),
                expected_authors[rank]
            )

    def test_author_rank(self):
        """
        Test if author rank is respected
        """
        # Execute the command
        self.cmd.handle(self.bibtex_file)

        # Case 1
        entry = Entry.objects.get(
            title=u'Mobyle: a new full web bioinformatics framework'
        )
        expected_authors = [
            u'Néron B',
            u'Ménager H',
            u'Maufrais C',
            u'Joly N',
            u'Maupetit J',
            u'Letort S',
            u'Carrere S',
            u'Tuffery P',
            u'Letondal C',
        ]
        self._test_entry_authors(entry, expected_authors)

        # Case 2
        entry = Entry.objects.get(title__startswith=u'fpocket')
        expected_authors = [
            u'Schmidtke P',
            u'Le Guilloux V',
            u'Maupetit J',
            u'Tufféry P'
        ]
        self._test_entry_authors(entry, expected_authors)

    def test_partial_publication_date(self):
        """Test if partial publication date flag"""
        # Execute the command
        self.cmd.handle(self.bibtex_file)

        qs = Entry.objects.filter(is_partial_publication_date=False)
        self.assertEqual(qs.count(), 1)

        qs = Entry.objects.filter(is_partial_publication_date=True)
        self.assertEqual(qs.count(), 8)
