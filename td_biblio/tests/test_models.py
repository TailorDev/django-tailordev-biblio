# -*- coding: utf-8 -*-
"""
TailorDev Bibliography

Test models.
"""
from django.test import TestCase

from ..factories import AuthorFactory


class AuthorModelTest(TestCase):
    """
    Tests for the Author model
    """

    def test_unicode(self):
        """
        Test __unicode__ method
        """
        author = AuthorFactory()
        self.assertEqual(unicode(author), author.get_formatted_name())
