# -*- coding: utf-8 -*-
"""
TailorDev Bibliography

Test models.
"""
from django.test import TestCase

from ..factories import (AuthorFactory, EditorFactory, JournalFactory,
    PublisherFactory, EntryFactory, CollectionFactory)
from ..models import Author, Editor, Journal, Publisher, Entry, Collection


class ModelTestMixin(object):
    """
    A simple mixin for models.

    You will need to override the `concrete_setup` method in child classes to
    setup the concrete model and the related factory.
    """
    def __init__(self, *args, **kwargs):
        """
        Setup the concrete model and factory
        """
        self.concrete_setup()
        super(ModelTestMixin, self).__init__(*args, **kwargs)

    def concrete_setup(self):
        """
        This is where you should work!
        """
        self.model = None
        self.factory = None
        raise NotImplementedError

    def test_saving_and_retrieving_items(self):
        """
        Test saving and retrieving two different objects
        """
        saved1 = self.factory()
        saved2 = self.factory()

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 2)

        self.assertEqual(qs[0], saved1)
        self.assertEqual(qs[1], saved2)


class AbstractHumanModelTestMixin(ModelTestMixin):
    """
    Tests for the abstract Human model
    """
    def test_unicode(self):
        """
        Test __unicode__ method
        """
        human = self.factory()
        self.assertEqual(unicode(human), human.get_formatted_name())

    def test_saving_and_retrieving_items(self):
        """
        Test saving and retrieving two Humans with different names
        """
        saved_human1 = self.model.objects.create(first_name="John",
                                                 last_name="McClane")
        saved_human2 = self.model.objects.create(first_name="Holly",
                                                 last_name="Gennero")

        humans = self.model.objects.all()
        self.assertEqual(humans.count(), 2)

        self.assertEqual(humans[0], saved_human1)
        self.assertEqual(humans[1], saved_human2)

    def test_set_first_initial(self):
        """
        Test the _set_first_initial method
        """
        human = self.factory(first_name="John", last_name="McClane")
        self.assertEqual(human.first_initial, "J")

        human = self.factory(first_name="John Jack Junior",
                             last_name="McClane")
        self.assertEqual(human.first_initial, "J J J")

    def test_get_formatted_name(self):
        """
        Test the get_formatted_name method
        """
        human = self.factory(first_name="John", last_name="McClane")
        formatted_name = human.get_formatted_name()
        expected = "McClane J"
        self.assertEqual(formatted_name, expected)


class AuthorModelTest(AbstractHumanModelTestMixin, TestCase):
    """
    Tests for the Author model
    """
    def concrete_setup(self):
        self.model = Author
        self.factory = AuthorFactory


class EditorModelTest(AbstractHumanModelTestMixin, TestCase):
    """
    Tests for the Editor model
    """
    def concrete_setup(self):
        self.model = Editor
        self.factory = EditorFactory


class AbstractEntityModelTestMixin(ModelTestMixin):
    """
    Tests for the abstract Entity model
    """
    def test_unicode(self):
        """
        Test __unicode__ method
        """
        entity = self.factory()
        self.assertEqual(unicode(entity), entity.name)


class JournalModelTest(AbstractEntityModelTestMixin, TestCase):
    """
    Tests for the Journal model
    """
    def concrete_setup(self):
        self.model = Journal
        self.factory = JournalFactory


class PublisherModelTest(AbstractEntityModelTestMixin, TestCase):
    """
    Tests for the Journal model
    """
    def concrete_setup(self):
        self.model = Publisher
        self.factory = PublisherFactory


class EntryModelTest(ModelTestMixin, TestCase):
    """
    Tests for the Entry model
    """
    def concrete_setup(self):
        self.model = Entry
        self.factory = EntryFactory

    def test_unicode(self):
        """
        Test __unicode__ method
        """
        entry = self.factory()
        self.assertEqual(unicode(entry), entry.title)


class CollectionModelTest(ModelTestMixin, TestCase):
    """
    Tests for the Collection model
    """
    def concrete_setup(self):
        self.model = Collection
        self.factory = CollectionFactory

    def test_unicode(self):
        """
        Test __unicode__ method
        """
        collection = self.factory()
        self.assertEqual(unicode(collection), collection.name)

    def test_add_entries(self):
        """
        Save a new collection with multiple entries
        """
        # Create entries
        for i in xrange(5):
            EntryFactory()

        # Create a collection
        collection = self.factory(entries=Entry.objects.all())

        self.assertEqual(collection.entries.count(), 5)
