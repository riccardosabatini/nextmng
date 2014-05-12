# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestSubject'
        db.create_table(u'main_testsubject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('mail', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['TestSubject'])

        # Adding model 'Experiment'
        db.create_table(u'main_experiment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='experiment', to=orm['main.TestSubject'])),
            ('executed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('m_objects', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('m_vegetables', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('m_sweets', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('m_fruits', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('m_stages', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('m_positives', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('m_salties', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Experiment'])

        # Adding model 'DbLock'
        db.create_table(u'main_dblock', (
            ('key', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('timeout', self.gf('django.db.models.fields.IntegerField')()),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['DbLock'])


    def backwards(self, orm):
        # Deleting model 'TestSubject'
        db.delete_table(u'main_testsubject')

        # Deleting model 'Experiment'
        db.delete_table(u'main_experiment')

        # Deleting model 'DbLock'
        db.delete_table(u'main_dblock')


    models = {
        u'main.dblock': {
            'Meta': {'object_name': 'DbLock'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {})
        },
        u'main.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'executed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm_fruits': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_objects': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_positives': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_salties': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_stages': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_sweets': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_vegetables': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experiment'", 'to': u"orm['main.TestSubject']"})
        },
        u'main.testsubject': {
            'Meta': {'ordering': "['registered']", 'object_name': 'TestSubject'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['main']