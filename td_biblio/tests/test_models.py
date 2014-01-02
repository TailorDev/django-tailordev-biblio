# -*- coding: utf-8 -*-
"""
TailorDev Bibliography

Test models.
"""
import datetime

from django.contrib.auth import get_user_model
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

    def concrete_setup(self):   # pragma: no cover
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

    def test_set_first_initial(self):
        """
        Test the _set_first_initial method
        """
        human = self.factory(first_name="John", last_name="McClane")
        self.assertEqual(human.first_initial, "J")

        human = self.factory(first_name="John Jack Junior",
                             last_name="McClane")
        self.assertEqual(human.first_initial, "J J J")

        human.first_name = "Jumping Jack Flash"
        human._set_first_initial()
        self.assertEqual(human.first_initial, "J J J")

        human.first_name = "Jumping Jack Flash"
        human._set_first_initial(force=True)
        self.assertEqual(human.first_initial, "J J F")

    def test_get_formatted_name(self):
        """
        Test the get_formatted_name method
        """
        human = self.factory(first_name="John", last_name="McClane")
        formatted_name = human.get_formatted_name()
        expected = "McClane J"
        self.assertEqual(formatted_name, expected)

    def test_user_linking(self):
        """
        Test linking the AbstractHuman object with a django user
        """
        user = get_user_model().objects.create(username='johnmcclane')
        human = self.factory(first_name="John",
                             last_name="McClane",
                             user=user)
        self.assertEqual(human.user, user)


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
        AuthorFactory(first_name='John', last_name='McClane')
        AuthorFactory(first_name='Holly', last_name='Gennero')
        journal = JournalFactory(name='Die Hard', abbreviation='Die Hard')

        entry = self.factory(
            authors=Author.objects.all(),
            title='Yippee-ki-yay, motherfucker',
            journal=journal,
            volume='1',
            pages='1--132',
            publication_date=datetime.date(1988, 7, 15)
        )
        expected = 'McClane J, and Gennero H, "Yippee-ki-yay, motherfucker", '
        expected += 'in Die Hard, vol. 1, pp. 1--132, July 1988.'
        self.assertEqual(unicode(entry), expected)

    def test_saving_and_retrieving_items(self):
        """
        Test saving and retrieving two different objects
        """
        saved1 = self.factory(publication_date=datetime.date(2012, 1, 2))
        saved2 = self.factory(publication_date=datetime.date(2011, 3, 12))

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 2)

        self.assertEqual(qs[0], saved1)
        self.assertEqual(qs[1], saved2)

    def test_ordering(self):
        """
        Test ordering when saving and retrieving two different objects
        """
        saved1 = self.factory(publication_date=datetime.date(2011, 1, 2))
        saved2 = self.factory(publication_date=datetime.date(2012, 3, 12))

        qs = self.model.objects.all()
        self.assertEqual(qs.count(), 2)

        self.assertEqual(qs[0], saved2)
        self.assertEqual(qs[1], saved1)

    def test_first_author(self):
        """
        Test the first_author method
        """
        entry = self.factory()
        self.assertEqual(entry.first_author(), '')

        # Generate authors
        author1 = AuthorFactory()
        for i in range(2):
            AuthorFactory()

        entry = self.factory(authors=Author.objects.all())
        self.assertEqual(entry.first_author(), author1)


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
