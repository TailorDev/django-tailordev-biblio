# -*- coding: utf-8 -*-
import datetime

from django.views.generic import ListView

from .models import Entry


class EntryListView(ListView):
    """Entry list view"""
    model = Entry
    paginate_by = 20
    template = 'td_biblio/entry_list.html'

    def get_queryset(self):
        """
        Add GET requests filters
        """
        filters = dict()

        # -- Publication year
        year = self.request.GET.get('year', None)
        # Is it an integer?
        try:
            self.current_publication_date = datetime.date(int(year), 1, 1)
        except:
            self.current_publication_date = None
        if year:
            filters['publication_date__year'] = year

        # Base queryset
        qs = super(EntryListView, self).get_queryset()

        # Return filtered queryset
        return qs.filter(**filters)

    def get_context_data(self, **kwargs):
        """
        Add filtering data to context
        """
        ctx = super(EntryListView, self).get_context_data(**kwargs)

        # -- Filters
        # publication date
        ctx['n_publications_total'] = Entry.objects.count()
        ctx['n_publications_filter'] = self.get_queryset().count()
        ctx['publication_years'] = Entry.objects.dates('publication_date',
                                                       'year', order='DESC')
        ctx['current_publication_year'] = self.current_publication_date

        return ctx
