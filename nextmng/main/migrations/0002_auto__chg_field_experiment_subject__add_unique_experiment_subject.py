# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Experiment.subject'
        db.alter_column(u'main_experiment', 'subject_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['main.TestSubject']))
        # Adding unique constraint on 'Experiment', fields ['subject']
        db.create_unique(u'main_experiment', ['subject_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Experiment', fields ['subject']
        db.delete_unique(u'main_experiment', ['subject_id'])


        # Changing field 'Experiment.subject'
        db.alter_column(u'main_experiment', 'subject_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TestSubject']))

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
            'subject': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'experiment'", 'unique': 'True', 'to': u"orm['main.TestSubject']"})
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