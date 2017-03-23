# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from td_biblio.utils.managers import bibtex_import


class Command(BaseCommand):
    help = "Import entries from a BibTex file"

    def add_arguments(self, parser):
        parser.add_argument(
            'bibtex',
            help="The path to the BibTeX file to import"
        )

    def handle(self, *args, **options):
        bibtex = options.get('bibtex', None)
        self.stdout.write("Importing '{}' BibTeX file...".format(bibtex))
        bibtex_import(bibtex)
        self.stdout.write(self.style.SUCCESS("Importation succeeded"))
