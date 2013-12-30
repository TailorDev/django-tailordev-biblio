# -*- coding: utf-8 -*-
from django.views.generic import ListView

from .models import Entry


class EntryListView(ListView):
    """Entry list view"""
    model = Entry
    template = 'td_biblio/entry_list.html'
