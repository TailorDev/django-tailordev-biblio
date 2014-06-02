# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'td_biblio_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_initial', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Member'], null=True, blank=True)),
        ))
        db.send_create_signal(u'td_biblio', ['Author'])

        # Adding model 'Editor'
        db.create_table(u'td_biblio_editor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_initial', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Member'], null=True, blank=True)),
        ))
        db.send_create_signal(u'td_biblio', ['Editor'])

        # Adding model 'Journal'
        db.create_table(u'td_biblio_journal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'td_biblio', ['Journal'])

        # Adding model 'Publisher'
        db.create_table(u'td_biblio_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'td_biblio', ['Publisher'])

        # Adding model 'Entry'
        db.create_table(u'td_biblio_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='article', max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['td_biblio.Journal'])),
            ('publication_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('pmid', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('booktitle', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='entries', null=True, to=orm['td_biblio.Publisher'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('annote', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'td_biblio', ['Entry'])

        # Adding M2M table for field editors on 'Entry'
        m2m_table_name = db.shorten_name(u'td_biblio_entry_editors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm[u'td_biblio.entry'], null=False)),
            ('editor', models.ForeignKey(orm[u'td_biblio.editor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['entry_id', 'editor_id'])

        # Adding M2M table for field crossref on 'Entry'
        m2m_table_name = db.shorten_name(u'td_biblio_entry_crossref')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_entry', models.ForeignKey(orm[u'td_biblio.entry'], null=False)),
            ('to_entry', models.ForeignKey(orm[u'td_biblio.entry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_entry_id', 'to_entry_id'])

        # Adding model 'Collection'
        db.create_table(u'td_biblio_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'td_biblio', ['Collection'])

        # Adding M2M table for field entries on 'Collection'
        m2m_table_name = db.shorten_name(u'td_biblio_collection_entries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm[u'td_biblio.collection'], null=False)),
            ('entry', models.ForeignKey(orm[u'td_biblio.entry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['collection_id', 'entry_id'])

        # Adding model 'AuthorEntryRank'
        db.create_table(u'td_biblio_authorentryrank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['td_biblio.Author'])),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['td_biblio.Entry'])),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'td_biblio', ['AuthorEntryRank'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'td_biblio_author')

        # Deleting model 'Editor'
        db.delete_table(u'td_biblio_editor')

        # Deleting model 'Journal'
        db.delete_table(u'td_biblio_journal')

        # Deleting model 'Publisher'
        db.delete_table(u'td_biblio_publisher')

        # Deleting model 'Entry'
        db.delete_table(u'td_biblio_entry')

        # Removing M2M table for field editors on 'Entry'
        db.delete_table(db.shorten_name(u'td_biblio_entry_editors'))

        # Removing M2M table for field crossref on 'Entry'
        db.delete_table(db.shorten_name(u'td_biblio_entry_crossref'))

        # Deleting model 'Collection'
        db.delete_table(u'td_biblio_collection')

        # Removing M2M table for field entries on 'Collection'
        db.delete_table(db.shorten_name(u'td_biblio_collection_entries'))

        # Deleting model 'AuthorEntryRank'
        db.delete_table(u'td_biblio_authorentryrank')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'directory.laboratory': {
            'Meta': {'ordering': "['title']", 'object_name': 'Laboratory'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_sharing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assistant_directors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'codirected_laboratories'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['directory.Member']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Member']", 'null': 'True', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'related_name': "'laboratory'", 'symmetrical': 'False', 'to': u"orm['td_cms.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'laboratories'", 'null': 'True', 'to': u"orm['directory.Member']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'is_highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '50'}),
            'synopsis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synopsis_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synopsis_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'directory.member': {
            'Meta': {'ordering': "['last_name', 'first_name', 'username']", 'object_name': 'Member'},
            'avatar': ('filebrowser.fields.FileBrowseField', [], {'default': "'uploads/images/avatar/default.png'", 'max_length': '200', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'has_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'members'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['directory.Platform']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'research': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'research_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'members'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['directory.Team']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'directory.platform': {
            'Meta': {'ordering': "['title']", 'object_name': 'Platform'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_sharing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Member']", 'null': 'True', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'related_name': "'platform'", 'symmetrical': 'False', 'to': u"orm['td_cms.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'is_highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'laboratory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'platforms'", 'null': 'True', 'to': u"orm['directory.Laboratory']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scientific_directors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'scientific_director_platforms'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['directory.Member']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '50'}),
            'synopsis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synopsis_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synopsis_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'technical_directors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'technical_director_platforms'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['directory.Member']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'directory.team': {
            'Meta': {'ordering': "['title']", 'object_name': 'Team'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_sharing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Member']", 'null': 'True', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'related_name': "'team'", 'symmetrical': 'False', 'to': u"orm['td_cms.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'detail_view_template': ('django.db.models.fields.CharField', [], {'default': "'td_lab/directory/team_detail.html'", 'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'is_highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'laboratory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'to': u"orm['directory.Laboratory']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'leaders': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'team_leader'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['directory.Member']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '50'}),
            'synopsis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synopsis_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synopsis_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'td_biblio.author': {
            'Meta': {'object_name': 'Author'},
            'first_initial': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Member']", 'null': 'True', 'blank': 'True'})
        },
        u'td_biblio.authorentryrank': {
            'Meta': {'ordering': "('rank',)", 'object_name': 'AuthorEntryRank'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['td_biblio.Author']"}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['td_biblio.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {})
        },
        u'td_biblio.collection': {
            'Meta': {'object_name': 'Collection'},
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collections'", 'symmetrical': 'False', 'to': u"orm['td_biblio.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'td_biblio.editor': {
            'Meta': {'object_name': 'Editor'},
            'first_initial': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Member']", 'null': 'True', 'blank': 'True'})
        },
        u'td_biblio.entry': {
            'Meta': {'ordering': "('-publication_date',)", 'object_name': 'Entry'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'annote': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entries'", 'symmetrical': 'False', 'through': u"orm['td_biblio.AuthorEntryRank']", 'to': u"orm['td_biblio.Author']"}),
            'booktitle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'crossref': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'crossref_rel_+'", 'blank': 'True', 'to': u"orm['td_biblio.Entry']"}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'entries'", 'blank': 'True', 'to': u"orm['td_biblio.Editor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['td_biblio.Journal']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'pmid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'to': u"orm['td_biblio.Publisher']"}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'article'", 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'td_biblio.journal': {
            'Meta': {'object_name': 'Journal'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'td_biblio.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'td_cms.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['td_cms.Category']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'visible_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['td_biblio']