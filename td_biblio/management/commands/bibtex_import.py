# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand, CommandError

from td_biblio.utils.managers import bibtex_import


class Command(BaseCommand):
    args = '<my_biblio.bib)>'
    help = 'Import entries from a BibTex file'

    def handle(self, *args, **options):
        logger = self._get_logger()

        if not len(args):
            raise CommandError("No BibTex file provided")

        bibtex_file = args[0]

        # import
        logger.info("Starting BibTex import from: %s" % bibtex_file)

        bibtex_import(bibtex_file)

        logger.info("BibTex import was successfull")

    def _get_logger(self):
        logger = logging.getLogger('td_biblio')
        return logger
