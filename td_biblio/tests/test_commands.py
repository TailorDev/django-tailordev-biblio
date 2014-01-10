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

    def test_command(self):
        """
        Test python manage.py bibtex_import biblio.bib
        """
        cmd = bibtex_import.Command()

        # Without an input file to handle, cmd shoud assert a CommandError
        with self.assertRaises(CommandError):
            cmd.handle()

        cmd.handle(self.bibtex_file)

        # How many entries did we successfully import?
        self.assertEqual(Entry.objects.count(), 9)

        # How many journals?
        self.assertEqual(Journal.objects.count(), 5)

        # How many authors?
        self.assertEqual(Author.objects.count(), 31)
