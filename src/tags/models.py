import datetime
from django.db import models
from django.db.models import F
from django.template.defaultfilters import slugify
from django_mongodb_engine.contrib import MongoDBManager
from djangotoolbox.fields import EmbeddedModelField

class TagManager(MongoDBManager):
    def create_or_update_count(self, tagname, obj):
        #Unhappy. This is not atomic, will have to be somehow refactored.
        slug = slugify(tagname)
        tag, created = self.get_or_create(name=tagname, slug=slug)
        tag.objects_count += 1
        tag.last_object = obj
        tag.save()
        return tag



class Tag(models.Model):
    slug = models.SlugField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now=True)
    last_object = EmbeddedModelField(null=True)
    objects_count = models.PositiveIntegerField(default=0, db_index=True)
    objects = TagManager()

    def __unicode__(self):
        return self.name

    class Meta:
        get_latest_by = 'last_updated'
        ordering = ['last_updated']