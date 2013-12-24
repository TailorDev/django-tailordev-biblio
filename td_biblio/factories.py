# -*- coding: utf-8 -*-
import names

from factory.django import DjangoModelFactory

from . import models


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


class PublisherFactory(AbstractEntityFactory):
    FACTORY_FOR = models.Publisher


class EntryFactory(DjangoModelFactory):
    FACTORY_FOR = models.Entry


class CollectionFactory(DjangoModelFactory):
    FACTORY_FOR = models.Collection
