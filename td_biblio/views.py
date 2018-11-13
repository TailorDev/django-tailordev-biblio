# -*- coding: utf-8 -*-
import datetime
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView
from django.views.generic.edit import FormMixin

from .exceptions import DOILoaderError, PMIDLoaderError
from .forms import AuthorDuplicatesForm, EntryBatchImportForm
from .models import Author, Collection, Entry, Journal
from .utils.loaders import DOILoader, PubmedLoader

logger = logging.getLogger("td_biblio")


def superuser_required(function=None):
    """
    Decorator for views that checks that the user is a super user redirecting
    to the log-in page if necessary.

    Inspired by Django 'login_required' decorator
    """
    actual_decorator = user_passes_test(lambda u: u.is_superuser)
    if function:
        return actual_decorator(function)
    return actual_decorator


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class SuperuserRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(SuperuserRequiredMixin, cls).as_view(**initkwargs)
        return superuser_required(view)


class EntryListView(ListView):
    """Entry list view"""

    model = Entry
    paginate_by = 20
    template = "td_biblio/entry_list.html"

    def get(self, request, *args, **kwargs):
        """Check GET request parameters validity and store them"""

        # -- Publication year
        year = self.request.GET.get("year", None)
        if year is not None:
            try:
                year = datetime.date(int(year), 1, 1)
            except ValueError:
                year = None
        self.current_publication_date = year

        # -- Publication author
        author = self.request.GET.get("author", None)
        if author is not None:
            try:
                author = int(author)
            except ValueError:
                author = None
        self.current_publication_author = author

        # -- Publication collection
        collection = self.request.GET.get("collection", None)
        if collection is not None:
            try:
                collection = int(collection)
            except ValueError:
                collection = None
        self.current_publication_collection = collection

        return super(EntryListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Add GET requests filters
        """
        filters = dict()

        # Publication date
        if self.current_publication_date:
            year = self.current_publication_date.year
            filters["publication_date__year"] = year

        # Publication authors
        if self.current_publication_author:
            author = Author.objects.get(id=self.current_publication_author)
            aliases = list(author.aliases.values_list("id", flat=True))
            filters["authors__id__in"] = [author.id] + aliases

        # Publication collection
        if self.current_publication_collection:
            filters["collections__id"] = self.current_publication_collection

        # Base queryset
        qs = super(EntryListView, self).get_queryset()

        # Return filtered queryset
        return qs.filter(**filters)

    def get_context_data(self, **kwargs):
        """
        Add filtering data to context
        """
        ctx = super(EntryListView, self).get_context_data(**kwargs)

        # -- Metrics
        # Publications (Entries)
        ctx["n_publications_total"] = Entry.objects.count()
        ctx["n_publications_filter"] = self.get_queryset().count()

        # Authors (from selected entries)
        ctx["n_authors_total"] = Author.objects.filter(alias=None).count()
        author_ids = self.get_queryset().values_list("authors__id", flat=True)
        author_ids = list(set(author_ids))
        filtered_authors = Author.objects.filter(id__in=author_ids, alias=None)
        ctx["n_authors_filter"] = filtered_authors.count()

        # Journals (Entries)
        ctx["n_journals_total"] = Journal.objects.count()
        journal_ids = self.get_queryset().values_list("journal__id", flat=True)
        journal_ids = list(set(journal_ids))
        ctx["n_journals_filter"] = len(journal_ids)

        # -- Filters
        # publication date
        ctx["publication_years"] = self.get_queryset().dates(
            "publication_date", "year", order="DESC"
        )
        ctx["current_publication_year"] = self.current_publication_date

        # Publication author
        authors_order = ("last_name", "first_name")
        ctx["publication_authors"] = filtered_authors.order_by(*authors_order)
        ctx["current_publication_author"] = self.current_publication_author

        # Publication collection
        ctx["publication_collections"] = Collection.objects.all()
        ctx[
            "current_publication_collection"
        ] = self.current_publication_collection  # noqa

        return ctx


class EntryBatchImportView(LoginRequiredMixin, SuperuserRequiredMixin, FormView):

    form_class = EntryBatchImportForm
    template_name = "td_biblio/entry_import.html"
    success_url = reverse_lazy("td_biblio:entry_list")

    def form_valid(self, form):
        """Save to database"""
        # PMIDs
        pmids = form.cleaned_data["pmids"]
        if len(pmids):
            pm_loader = PubmedLoader()

            try:
                pm_loader.load_records(PMIDs=pmids)
            except PMIDLoaderError as e:
                messages.error(self.request, e)
                return self.form_invalid(form)

            pm_loader.save_records()

        # DOIs
        dois = form.cleaned_data["dois"]
        if len(dois):
            doi_loader = DOILoader()

            try:
                doi_loader.load_records(DOIs=dois)
            except DOILoaderError as e:
                messages.error(self.request, e)
                return self.form_invalid(form)

            doi_loader.save_records()

        messages.success(
            self.request,
            _("We have successfully imported {} reference(s).").format(
                len(dois) + len(pmids)
            ),
        )

        return super(EntryBatchImportView, self).form_valid(form)


class FindDuplicatedAuthorsView(
    LoginRequiredMixin, SuperuserRequiredMixin, FormMixin, ListView
):

    form_class = AuthorDuplicatesForm
    model = Author
    ordering = ("last_name", "first_name")
    paginate_by = 30
    queryset = Author.objects.filter(alias=None)
    success_url = reverse_lazy("td_biblio:duplicates")
    template_name = "td_biblio/find_duplicated_authors.html"

    def _add_aliases(self, authors, alias):
        return authors.update(alias=alias)

    def form_valid(self, form):

        authors = form.cleaned_data["authors"]
        alias = form.cleaned_data["alias"]
        match = self._add_aliases(authors, alias)

        messages.success(
            self.request,
            _("Added '{}' as alias for {} author(s).").format(
                alias.get_formatted_name(), match
            ),
        )

        return super(FindDuplicatedAuthorsView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        ctx = super(FindDuplicatedAuthorsView, self).get_context_data(**kwargs)
        ctx.update({"paginate_by": self.get_paginate_by(self.queryset)})
        return ctx

    def get_paginate_by(self, queryset):

        by = self.request.GET.get("by", None)
        if not by:
            return self.paginate_by
        try:
            return int(by)
        except ValueError:
            pass

    def get_success_url(self):
        """Add get parameters"""
        url = force_text(self.success_url)
        if self.request.GET:
            url = "{}?{}".format(url, self.request.GET.urlencode())
        return url

    def post(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
