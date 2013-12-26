# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Author, Editor, Journal, Publisher, Entry, Collection


class AbstractHumanAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')


class AuthorAdmin(AbstractHumanAdmin):
    pass


class EditorAdmin(AbstractHumanAdmin):
    pass


class JournalAdmin(admin.ModelAdmin):
    pass


class PublisherAdmin(admin.ModelAdmin):
    pass


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'publication_date', 'journal')
    list_filter = ('publication_date', 'journal', 'authors')
    date_hierarchy = 'publication_date'


class CollectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Collection, CollectionAdmin)
