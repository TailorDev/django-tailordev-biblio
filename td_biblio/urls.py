# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import EntryListView


urlpatterns = [
    # Entry List
    url('^$', EntryListView.as_view(), name='entry_list'),
]
