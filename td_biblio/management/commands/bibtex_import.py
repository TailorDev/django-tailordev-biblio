# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand, CommandError

from td_biblio.utils.managers import bibtex_import


class Command(BaseCommand):
    args = '<BibTex file (.bib)>'
    help = 'Generates lorem ipsum fixtures for designers'

    def handle(self, *args, **options):
        #logger = self._get_logger()

        if not len(args):
            raise CommandError("No BibTex file provided")

        # import
        bibtex_import(args[0])

    def _get_logger(self):
        logger = logging.getLogger('td_biblio')
        return logger
