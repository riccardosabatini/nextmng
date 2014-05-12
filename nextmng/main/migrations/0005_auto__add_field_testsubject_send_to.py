# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TestSubject.send_to'
        db.add_column(u'main_testsubject', 'send_to',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TestSubject.send_to'
        db.delete_column(u'main_testsubject', 'send_to')


    models = {
        u'main.aggregation': {
            'Meta': {'object_name': 'Aggregation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm_fruits': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_objects': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_positives': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_salties': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_stages': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_sweets': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'm_vegetables': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
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
            'pdf_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'send_to': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['main']