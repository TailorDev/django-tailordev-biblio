# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Author, Editor, Journal, Publisher, Entry, Collection


class AbstractHumanAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    ordering = ('last_name', 'first_name')


class AuthorAdmin(AbstractHumanAdmin):
    pass


class EditorAdmin(AbstractHumanAdmin):
    pass


class AbstractEntityAdmin(admin.ModelAdmin):
    ordering = ('name',)


class JournalAdmin(AbstractEntityAdmin):
    pass


class PublisherAdmin(AbstractEntityAdmin):
    pass


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_author', 'type', 'publication_date',
                    'journal')
    list_filter = ('publication_date', 'journal', 'authors')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    fieldsets = (
        ('Publication core fields', {
            'fields': ('type', 'title', 'authors', 'journal',
                       ('volume', 'number'), ('pages', 'publication_date'),
                       'url')
        }),
        ('Identifiers', {
            'fields': (('doi', 'issn'), ('isbn', 'pmid'))
        }),
        ('Book fields', {
            'fields': ('booktitle', 'edition', 'chapter')
        }),
        ('PhD Thesis', {
            'fields': ('school',)
        }),
        ('Proceedings', {
            'fields': ('organization',)
        }),
        ('Miscellaneous', {
            'fields': ('editors', 'publisher', 'address', 'annote', 'note')
        }),
    )


class CollectionAdmin(admin.ModelAdmin):

    def size(self, obj):
        """Get the number of entries in each collection"""
        return obj.entries.count()

    list_display = ('name', 'size')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Collection, CollectionAdmin)
