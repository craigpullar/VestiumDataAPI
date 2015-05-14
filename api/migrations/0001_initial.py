# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photo'
        db.create_table(u'api_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'api', ['Photo'])

        # Adding model 'User'
        db.create_table(u'api_user', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('lastIpAddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('profileImageSlug', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('profileImagePath', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['User'])

        # Adding model 'BetaCode'
        db.create_table(u'api_betacode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'api', ['BetaCode'])

        # Adding model 'Brand'
        db.create_table(u'api_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'api', ['Brand'])

        # Adding model 'Post'
        db.create_table(u'api_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imageSlug', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('imagePath', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
            ('pubDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('pastel', self.gf('django.db.models.fields.IntegerField')()),
            ('numLikes', self.gf('django.db.models.fields.IntegerField')()),
            ('numComments', self.gf('django.db.models.fields.IntegerField')()),
            ('flagged', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'api', ['Post'])

        # Adding model 'SponsoredPost'
        db.create_table(u'api_sponsoredpost', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['api.Post'], unique=True, primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Brand'])),
        ))
        db.send_create_signal(u'api', ['SponsoredPost'])

        # Adding model 'Comment'
        db.create_table(u'api_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Post'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('pubDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['Comment'])

        # Adding model 'Relationship'
        db.create_table(u'api_relationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follower', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_follower', to=orm['api.User'])),
            ('following', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_following', to=orm['api.User'])),
            ('followDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'api', ['Relationship'])

        # Adding model 'Like'
        db.create_table(u'api_like', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Post'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
        ))
        db.send_create_signal(u'api', ['Like'])

        # Adding model 'Label'
        db.create_table(u'api_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')()),
            ('y', self.gf('django.db.models.fields.IntegerField')()),
            ('angle', self.gf('django.db.models.fields.IntegerField')()),
            ('colour', self.gf('django.db.models.fields.CharField')(default='black', max_length=10, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('imageSlug', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('imagePath', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('GeoPosition', self.gf('geoposition.fields.GeopositionField')(max_length=42)),
            ('pubDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['Label'])

        # Adding model 'ItemTag'
        db.create_table(u'api_itemtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Label'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'api', ['ItemTag'])

        # Adding model 'PostTag'
        db.create_table(u'api_posttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Post'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'api', ['PostTag'])

        # Adding model 'NotificationType'
        db.create_table(u'api_notificationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['NotificationType'])

        # Adding model 'Notification'
        db.create_table(u'api_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.NotificationType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
            ('pubDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Post'])),
            ('seen', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'api', ['Notification'])

        # Adding model 'LoginLog'
        db.create_table(u'api_loginlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
            ('loginDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ipAddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
        ))
        db.send_create_signal(u'api', ['LoginLog'])

        # Adding model 'LogoutLog'
        db.create_table(u'api_logoutlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.User'])),
            ('logoutDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['LogoutLog'])


    def backwards(self, orm):
        # Deleting model 'Photo'
        db.delete_table(u'api_photo')

        # Deleting model 'User'
        db.delete_table(u'api_user')

        # Deleting model 'BetaCode'
        db.delete_table(u'api_betacode')

        # Deleting model 'Brand'
        db.delete_table(u'api_brand')

        # Deleting model 'Post'
        db.delete_table(u'api_post')

        # Deleting model 'SponsoredPost'
        db.delete_table(u'api_sponsoredpost')

        # Deleting model 'Comment'
        db.delete_table(u'api_comment')

        # Deleting model 'Relationship'
        db.delete_table(u'api_relationship')

        # Deleting model 'Like'
        db.delete_table(u'api_like')

        # Deleting model 'Label'
        db.delete_table(u'api_label')

        # Deleting model 'ItemTag'
        db.delete_table(u'api_itemtag')

        # Deleting model 'PostTag'
        db.delete_table(u'api_posttag')

        # Deleting model 'NotificationType'
        db.delete_table(u'api_notificationtype')

        # Deleting model 'Notification'
        db.delete_table(u'api_notification')

        # Deleting model 'LoginLog'
        db.delete_table(u'api_loginlog')

        # Deleting model 'LogoutLog'
        db.delete_table(u'api_logoutlog')


    models = {
        u'api.betacode': {
            'Meta': {'object_name': 'BetaCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.brand': {
            'Meta': {'object_name': 'Brand'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Post']"}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.itemtag': {
            'Meta': {'object_name': 'ItemTag'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Label']"})
        },
        u'api.label': {
            'GeoPosition': ('geoposition.fields.GeopositionField', [], {'max_length': '42'}),
            'Meta': {'object_name': 'Label'},
            'angle': ('django.db.models.fields.IntegerField', [], {}),
            'colour': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '10', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagePath': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'imageSlug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {})
        },
        u'api.like': {
            'Meta': {'object_name': 'Like'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.loginlog': {
            'Meta': {'object_name': 'LoginLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipAddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'loginDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.logoutlog': {
            'Meta': {'object_name': 'LogoutLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logoutDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.notification': {
            'Meta': {'object_name': 'Notification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Post']"}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'seen': ('django.db.models.fields.BooleanField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.NotificationType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.notificationtype': {
            'Meta': {'object_name': 'NotificationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.photo': {
            'Meta': {'object_name': 'Photo'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'api.post': {
            'Meta': {'object_name': 'Post'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagePath': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'imageSlug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'numComments': ('django.db.models.fields.IntegerField', [], {}),
            'numLikes': ('django.db.models.fields.IntegerField', [], {}),
            'pastel': ('django.db.models.fields.IntegerField', [], {}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.User']"})
        },
        u'api.posttag': {
            'Meta': {'object_name': 'PostTag'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Post']"})
        },
        u'api.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'followDate': ('django.db.models.fields.DateTimeField', [], {}),
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_follower'", 'to': u"orm['api.User']"}),
            'following': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_following'", 'to': u"orm['api.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'api.sponsoredpost': {
            'Meta': {'object_name': 'SponsoredPost', '_ormbases': [u'api.Post']},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Brand']"}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['api.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'api.user': {
            'Meta': {'object_name': 'User', '_ormbases': [u'auth.User']},
            'lastIpAddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'profileImagePath': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profileImageSlug': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']