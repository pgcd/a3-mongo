from django.contrib.auth.models import User
from django.db import models
from django_mongodb_engine.contrib import MongoDBManager
from djangotoolbox.fields import ListField, EmbeddedModelField, SetField

# Create your models here.
class ProfilesManager(MongoDBManager):
    class Meta:
        use_for_related_fields = True


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', db_index=True)
    topics = ListField()
    objects = ProfilesManager()

    def __unicode__(self):
        return u"%s" % self.user