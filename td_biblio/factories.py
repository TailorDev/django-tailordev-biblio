# -*- coding: utf-8 -*-
import factory
import names

from factory.django import DjangoModelFactory

from . import models


JOURNAL_CHOICES = [
    ('Bioinformatics', 'Bioinformatics'),
    ('BMC Bioinf.', 'BMC Bioinformatics'),
    ('JACS', 'Journal of the American Chemical Society'),
    ('J. Comput. Chem.', 'Journal of Computational Chemistry'),
    ('Nat. Biotechnol.', 'Nature Biotechnology'),
    ('Nucleic Acids Res.', 'Nucleic Acids Research'),
    ('PNAS', 'Proceedings of the National Academy of Sciences of the United States of America'),  # NOPEP8
    ('Proteins Struct. Funct. Bioinf.', 'Proteins: Structure, Function, and Bioinformatics'),  # NOPEP8
]


class AbstractHuman(DjangoModelFactory):
    FACTORY_FOR = models.AbstractHuman
    ABSTRACT_FACTORY = True

    first_name = names.get_first_name()
    last_name = names.get_last_name()


class AuthorFactory(AbstractHuman):
    FACTORY_FOR = models.Author


class EditorFactory(AbstractHuman):
    FACTORY_FOR = models.Editor


class AbstractEntityFactory(DjangoModelFactory):
    FACTORY_FOR = models.AbstractEntity
    ABSTRACT_FACTORY = True


class JournalFactory(AbstractEntityFactory):
    FACTORY_FOR = models.Journal
    FACTORY_DJANGO_GET_OR_CREATE = ('abbreviation',)

    name = factory.Iterator(JOURNAL_CHOICES, getter=lambda c: c[1])
    abbreviation = factory.Iterator(JOURNAL_CHOICES, getter=lambda c: c[0])


class PublisherFactory(AbstractEntityFactory):
    FACTORY_FOR = models.Publisher


class EntryFactory(DjangoModelFactory):
    FACTORY_FOR = models.Entry


class CollectionFactory(DjangoModelFactory):
    FACTORY_FOR = models.Collection
