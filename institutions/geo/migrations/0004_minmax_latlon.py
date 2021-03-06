# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for tract in orm.StateCensusTract.objects.all():
            # Can't use auto_fields since we are using south's ORM
            lons, lats = zip(*[pt for polygon in tract.geom.coords
                               for line in polygon
                               for pt in line])
            tract.minlat = min(lats)
            tract.maxlat = max(lats)
            tract.minlon = min(lons)
            tract.maxlon = max(lons)
            tract.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'geo.statecensustract': {
            'Meta': {'object_name': 'StateCensusTract'},
            'aland': ('django.db.models.fields.FloatField', [], {}),
            'awater': ('django.db.models.fields.FloatField', [], {}),
            'countyfp': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'funcstat': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'geoid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '4269'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intptlat': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'intptlon': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'maxlon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_index': 'True'}),
            'maxlat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_index': 'True'}),
            'minlat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_index': 'True'}),
            'minlon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_index': 'True'}),
            'mtfcc': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'namelsad': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'statefp': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'tractce': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['geo']
    symmetrical = True
