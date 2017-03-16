# -*- coding: utf-8 -*-
"""
Django TailorDev Biblio

Test views
"""
import datetime
import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..factories import (CollectionFactory, EntryWithAuthorsFactory)
from ..models import Entry


@pytest.mark.django_db
class EntryListViewTests(TestCase):
    """
    Tests for the EntryListViewTests
    """
    def setUp(self):
        """
        Generate Author and Entry fixtures & set object level vars
        """
        self.url = reverse('entry_list')
        self.paginate_by = 20
        self.n_publications_per_year = 3
        self.start_year = 2000
        self.end_year = 2014
        self.n_publications = self.end_year - self.start_year
        self.n_publications *= self.n_publications_per_year
        self.n_authors = self.n_publications * 3
        self.publications_years = []
        self.max_page_num = self.n_publications / self.paginate_by
        if self.n_publications % self.paginate_by:
            self.max_page_num += 1

        # Entry (14 * 3 = 42)
        for y in range(self.start_year, self.end_year, 1):
            for i in range(1, 1 + self.n_publications_per_year):
                date = datetime.date(y, i, 1)
                EntryWithAuthorsFactory(publication_date=date)
                self.publications_years.append(y)

    def test_get(self):
        """
        Test the EntryListViewTests get method
        """
        response = self.client.get(self.url)

        # Standard response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('td_biblio/entry_list.html')

    def _test_one_page(self, page=1, **kwargs):
        """
        Test the get request pagination for one page.

        Use **kwargs to add request parameters.
        """
        params = {'page': page}
        params.update(kwargs)
        response = self.client.get(self.url, params)

        # Check the requested page number is within the proper range
        if page > self.max_page_num:
            self.assertEqual(response.status_code, 404)
            return

        # Standard response
        self.assertEqual(response.status_code, 200)

        # Publication list
        publication_block = '<li class="publication-list-year">'
        start = self.paginate_by * (page - 1)
        end = self.paginate_by * page
        if end > self.n_publications:
            end = self.n_publications
        expected_count = len(set(self.publications_years[start:end]))
        self.assertContains(response, publication_block,
                            count=expected_count)

        publication_block = '<li class="publication">'
        self.assertContains(response, publication_block,
                            count=end - start)

        # Pagination
        self.assertTrue(response.context['is_paginated'])

        pagination_block = '<div class="pagination-centered">'
        self.assertContains(response, pagination_block)

        pagination_block = '<a href="">%d</a>' % page
        self.assertContains(response, pagination_block)

    def _test_filtering(self, **kwargs):
        """Test entry list filtering"""
        params = dict()
        params.update(kwargs)
        response = self.client.get(self.url, params)

        # Standard response
        self.assertEqual(response.status_code, 200)

        # Display at list a publication
        publication_block = '<li class="publication">'
        self.assertContains(response, publication_block)

    def test_pagination(self):
        """
        Test the get request pagination for 4 pages
        """
        for page in range(1, 5):
            self._test_one_page(page=page)

    def test_year_filtering(self):
        """
        Test the get request with a year parameter
        """
        # Get a valid date
        entry = Entry.objects.get(id=1)
        params = {'year': entry.publication_date.year}

        self._test_filtering(**params)

    def test_author_filtering(self):
        """
        Test the get request with an author parameter
        """
        # Get a valid author
        entry = Entry.objects.get(id=1)
        params = {'author': entry.first_author.id}

        self._test_filtering(**params)

    def test_collection_filtering(self):
        """
        Test the get request with a collection parameter
        """
        # Create a collection
        entries = Entry.objects.filter(id__in=(1, 5, 10, 15))
        collection = CollectionFactory(entries=entries)

        # Get a valid collection
        params = {'collection': collection.id}

        self._test_filtering(**params)

    def test_collection_author_year_filtering(self):
        """
        Test the get request with a collection, an author and a year parameter
        """
        # Create a collection
        entries = Entry.objects.filter(id__in=(1, 5, 10, 15))
        collection = CollectionFactory(entries=entries)
        entry = Entry.objects.get(id=1)

        # Get a valid collection
        params = {
            'collection': collection.id,
            'author': entry.first_author.id,
            'year': entry.publication_date.year,
        }
        self._test_filtering(**params)

    def test_author_year_filtering(self):
        """
        Test the get request with an author and a year parameter
        """
        # Get a valid date
        entry = Entry.objects.get(id=1)
        params = {
            'author': entry.first_author.id,
            'year': entry.publication_date.year,
        }

        self._test_filtering(**params)

    def test_get_queryset(self):
        """
        Test the EntryListViewTests get_queryset method
        """
        year = 2012
        response = self.client.get(self.url, {'year': year})
        self.assertEqual(response.status_code, 200)

        # Context
        date = datetime.date(year, 1, 1)
        self.assertEqual(response.context['current_publication_year'], date)

        self.assertEqual(
            response.context['n_publications_filter'],
            self.n_publications_per_year)

    def test_get_context_data(self):
        """
        Test the EntryListViewTests get_context_data method
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Get all different publication years
        start = self.end_year - 1
        end = self.start_year - 1
        years_range = range(start, end, -1)
        publication_years = [datetime.date(y, 1, 1) for y in years_range]

        # Context
        self.assertEqual(
            response.context['n_publications_total'],
            self.n_publications)

        self.assertEqual(
            response.context['n_publications_filter'],
            self.n_publications)

        self.assertListEqual(
            list(response.context['publication_years']),
            publication_years)

        self.assertEqual(
            response.context['n_authors_total'],
            self.n_authors)

        self.assertEqual(
            response.context['publication_authors'].count(),
            self.n_authors)

        self.assertEqual(response.context['current_publication_year'], None)
