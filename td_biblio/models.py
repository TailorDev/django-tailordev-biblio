# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class AbstractHuman(models.Model):
    """Simple Abstract Human model

    Note that this model may be linked to django registered users
    """

    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    initials = models.CharField(_("Initials"), max_length=10, blank=True)

    # This is a django user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.get_formatted_name()

    def save(self, *args, **kwargs):
        """Set initials before saving"""

        self._set_first_name_initials()
        super(Author, self).save(*args, **kwargs)

    def _set_first_name_initials(self, force=False):
        """Set author initials"""

        if self.initials and not force:
            return self.initials
        self.initials = u" ".join([c[0] for c in self.first_name.split()])

    def get_full_name(self):
        """Return author formated full name, e.g. Maupetit J"""

        return u"%s %s" % (self.last_name, self.initials)


class Author(AbstractHuman):
    """Entry author"""

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Editor(AbstractHuman):
    """Journal or book editor"""

    class Meta:
        verbose_name = _("Editor")
        verbose_name_plural = _("Editors")


class AbstractEntity(models.Model):
    """Simple abstract entity"""

    name = models.CharField(_("Name"), max_length=150)
    abbreviation = models.CharField(_("Entity abbreviation"), max_length=100, blank=True, help_text=_("e.g. Proc Natl Acad Sci U S A"))

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Journal(AbstractEntity):
    """Peer reviewed journal"""

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")


class Publisher(AbstractEntity):
    """Journal or book publisher"""

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")


class Entry(models.Model):
    """The core model for references

    Largely guided by the BibTeX file format (see
    http://en.wikipedia.org/wiki/BibTeX).

    Unsupported fields (for now):

    * eprint: A specification of an electronic publication, often a preprint
      or a technical report
    * howpublished: How it was published, if the publishing method is
      nonstandard
    * institution: The institution that was involved in the publishing, but not
      necessarily the publisher
    * key: A hidden field used for specifying or overriding the alphabetical
      order of entries (when the "author" and "editor" fields are missing).
      Note that this is very different from the key (mentioned just after this
      list) that is used to cite or cross-reference the entry.
    * series: The series of books the book was published in (e.g. "The Hardy
      Boys" or "Lecture Notes in Computer Science")
    * type: The field overriding the default type of publication (e.g.
      "Research Note" for techreport, "{PhD} dissertation" for phdthesis,
      "Section" for inbook/incollection)
    """

    ARTICLE = 'article'
    BOOK = 'book'
    BOOKLET = 'booklet'
    CONFERENCE = 'conference'
    INBOOK = 'inbook'
    INCOLLECTION = 'incollection'
    INPROCEEDINGS = 'inproceedings'
    MANUAL = 'manual'
    MASTERSTHESIS = 'mastersthesis'
    MISC = 'misc'
    PHDTHESIS = 'phdthesis'
    PROCEEDINGS = 'proceedings'
    TECHREPORT = 'techreport'
    UNPUBLISHED = 'unpublished'

    ENTRY_TYPES_CHOICES = (
        (ARTICLE, _("Article")),
        (BOOK, _("Book")),
        (BOOKLET, _("Book (no publisher)")),
        (CONFERENCE, _("Conference")),
        (INBOOK, _("Book chapter")),
        (INCOLLECTION, _("Book from a collection")),
        (INPROCEEDINGS, _("Conference proceedings article")),
        (MANUAL, _("Technical documentation")),
        (MASTERSTHESIS, _("Master's Thesis")),
        (MISC, _("Miscellaneous")),
        (PHDTHESIS, _("PhD Thesis")),
        (PROCEEDINGS, _("Conference proceedings")),
        (TECHREPORT, _("Technical report")),
        (UNPUBLISHED, _("Unpublished work")),
    )

    type = models.CharField(_("Entry type"), max_length=50, choices=ENTRY_TYPES_CHOICES, default=ARTICLE)

    # Base fields
    title = models.CharField(_("Title"), max_length=255)
    authors = models.ManyToManyField('Author', related_name='entries')
    journal = models.ForeignKey('Journal', related_name='entries')
    publication_date = models.DateField(_("Publication date"), blank=True, null=True)
    volume = models.CharField(_("The volume of a journal or multi-volume book"), max_length=50, blank=True)
    number = models.CharField(_("Number"), max_length=50, blank=True, help_text=_("The '(issue) number' of a journal, magazine, or tech-report, if applicable. (Most publications have a 'volume', but no 'number' field.)"))
    pages = models.CharField(_("Page numbers, separated either by commas or double-hyphens"), max_length=50, blank=True)
    url = models.URLField(_("URL"), blank=True, help_text=_("The WWW address where to find this resource"))

    # Identifiers
    doi = models.CharField(_("DOI"), max_length=100, blank=True, help_text=_("Digital Object Identifier for this resource"))
    issn = models.CharField(_("ISSN"), max_length=20, blank=True, help_text=_("International Standard Serial Number"))
    isbn = models.CharField(_("ISBN"), max_length=20, blank=True, help_text=_("International Standard Book Number"))
    pmid = models.CharField(_("PMID"), blank=True, max_length=20, help_text=_("Pubmed ID"))

    # Book
    booktitle = models.CharField(_("Book title"), max_length=50, blank=True, help_text=_("The title of the book, if only part of it is being cited"))
    edition = models.CharField(_("Edition"), max_length=100, blank=True, help_text=_("The edition of a book, long form (such as 'First' or 'Second')"))
    chapter = models.CharField(_("Chapter number"), max_length=50, blank=True)

    # PhD Thesis
    school = models.CharField(_("School"), max_length=50, blank=True, help_text=_("The school where the thesis was written"))

    # Proceedings
    organization = models.CharField(_("Organization"), max_length=50, blank=True, help_text=_("The conference sponsor"))

    # Misc
    editors = models.ManyToManyField('Editor', related_name='entries')
    publisher = models.ForeignKey('Publisher', related_name='entries')
    address = models.CharField(_("Address"), max_length=250, blank=True, help_text=_("Publisher's address (usually just the city, but can be the full address for lesser-known publishers)"))
    annote = models.CharField(_("Annote"), max_length=250, blank=True, help_text=_("An annotation for annotated bibliography styles (not typical)"))
    note = models.TextField(_("Note"), blank=True, help_text=_("Miscellaneous extra information"))

    # Related publications
    crossref = models.ManyToManyField('self')

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    def __unicode__(self):
        return self.title


class Collection(models.Model):
    """Define a collection of entries"""

    name = models.CharField(_("Name"), max_length=100)
    short_description = models.TextField(_("Short description"), blank=True, null=True)
    entries = models.ManyToManyField('Entry', related_name="collections")

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")

    def __unicode__(self):
        return self.name
