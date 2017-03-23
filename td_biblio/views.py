# -*- coding: utf-8 -*-
import datetime

from django.views.generic import ListView

from .models import Author, Collection, Entry, Journal


class EntryListView(ListView):
    """Entry list view"""
    model = Entry
    paginate_by = 20
    template = 'td_biblio/entry_list.html'

    def get(self, request, *args, **kwargs):
        """Check GET request parameters validity and store them"""

        # -- Publication year
        year = self.request.GET.get('year', None)
        # Is it an integer?
        try:
            self.current_publication_date = datetime.date(int(year), 1, 1)
        except:
            self.current_publication_date = None

        # -- Publication author
        author = self.request.GET.get('author', None)
        # Is it an integer?
        try:
            self.current_publication_author = int(author)
        except:
            self.current_publication_author = None

        # -- Publication collection
        collection = self.request.GET.get('collection', None)
        # Is it an integer?
        try:
            self.current_publication_collection = int(collection)
        except:
            self.current_publication_collection = None

        return super(EntryListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Add GET requests filters
        """
        filters = dict()

        # Publication date
        if self.current_publication_date:
            year = self.current_publication_date.year
            filters['publication_date__year'] = year

        # Publication authors
        if self.current_publication_author:
            filters['authors__id'] = self.current_publication_author

        # Publication collection
        if self.current_publication_collection:
            filters['collections__id'] = self.current_publication_collection

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
        ctx['n_publications_total'] = Entry.objects.count()
        ctx['n_publications_filter'] = self.get_queryset().count()

        # Authors (from selected entries)
        ctx['n_authors_total'] = Author.objects.count()
        author_ids = self.get_queryset().values_list('authors__id', flat=True)
        author_ids = list(set(author_ids))
        filtered_authors = Author.objects.filter(id__in=author_ids)
        ctx['n_authors_filter'] = filtered_authors.count()

        # Journals (Entries)
        ctx['n_journals_total'] = Journal.objects.count()
        journal_ids = self.get_queryset().values_list('journal__id', flat=True)
        journal_ids = list(set(journal_ids))
        ctx['n_journals_filter'] = len(journal_ids)

        # -- Filters
        # publication date
        ctx['publication_years'] = self.get_queryset().dates(
            'publication_date',
            'year', order='DESC'
        )
        ctx['current_publication_year'] = self.current_publication_date

        # Publication author
        authors_order = ('last_name', 'first_name')
        ctx['publication_authors'] = filtered_authors.order_by(*authors_order)
        ctx['current_publication_author'] = self.current_publication_author

        # Publication collection
        ctx['publication_collections'] = Collection.objects.all()
        ctx['current_publication_collection'] = self.current_publication_collection  # noqa

        return ctx
