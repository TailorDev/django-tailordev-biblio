# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from .views import EntryListView


urlpatterns = patterns(
    '',

    # Entry List
    url('^$', EntryListView.as_view(), name='entry_list'),
)
