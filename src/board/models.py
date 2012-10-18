import datetime
import random
from bson import ObjectId
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum
from django.db import models
from django.db.models import permalink, F
from djangotoolbox.fields import ListField, EmbeddedModelField
from uuidfield import UUIDField
# Create your models here.
import time
from django_mongodb_engine.contrib import MongoDBManager



class PostManager(MongoDBManager):
    def createRubbish(self, topic=None):
        """
        :return: Post
        """
        p = Post()
        p.title = lorem_ipsum.words(random.randint(0, 5), False)
        p.body = p.body_markup = "<br/>\n".join(lorem_ipsum.paragraphs(random.randint(0, 7), False))
        p.summary = lorem_ipsum.paragraph()
        p.user = User.objects.all()[random.randint(0, 850)]
        if random.randint(1, 50) == 1:
            p.hidden = True
        if random.randint(1, 100) == 1:
            p.deleted = True
        return p


class Post(models.Model):
    #Data
    id = UUIDField(auto=True, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    body_markup = models.TextField(blank=True)
    summary = models.TextField(blank=True, default='')
    user = EmbeddedModelField(User, blank=True, null=True, db_index=True)
    deleted = models.BooleanField()
    hidden = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    rating = models.IntegerField(default=0)

    ip = models.IPAddressField(default='0.0.0.0')

    objects = PostManager()

    def __unicode__(self):
        if self.title:
            return u"%s [#%s]" % (self.title, self.pk,)
        else:
            return u"#%s" % self.pk

    def adjustRating(self, rating=0):
        Topic.objects.raw_update({"replies.id":self.id.hex},{"$inc":{"rating":rating, "replies.$.rating":rating}})
        return self

#    @permalink
#    def get_absolute_url(self):
#        return 'board_post_view', (self.pk,), {}

class TopicManager(MongoDBManager):
    def createRubbish(self, reply_chance=0.98):
        p = Post.objects.createRubbish()
        t = Topic(obj=p)
        for i in range(0, random.randint(0, 5)):
            t.tags.append(lorem_ipsum.words(random.randint(1, 2), False))
        if random.randint(0, 50) == 1:
            t.homepage = True
        t.deleted = p.deleted
        t.hidden = p.hidden
        while random.random() < reply_chance:
            t.replies.append(Post.objects.createRubbish())
        t.replies_count = len(t.replies)
        t.save()
        return t

    def topicize(self, obj):
        """
        Function to make a Topic out of any other object.
        """
        t = Topic(obj=obj)
        t.deleted = obj.deleted
        t.hidden = obj.hidden
        t.rating = obj.rating
        t.save()

#        t.obj.topic = t
#        t.obj.save()

class Topic(models.Model):
    homepage = models.BooleanField(db_index=True)
    hidden = models.BooleanField()
    deleted = models.BooleanField()
    tags = ListField(db_index=True)
    obj = EmbeddedModelField()
    replies = ListField(EmbeddedModelField(Post))
    objects = TopicManager()
    #    title = models.CharField(max_length=255, blank=True)
    #    body = models.TextField(blank=True)
    views_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)
    timeshift = models.IntegerField(default=0) #Mostly used for bookkeeping, but might be useful later
    timestamp = models.PositiveIntegerField(default=0, db_index=True)


    @property
    def title(self):
        return self.obj.title or self.pk

    @property
    def body(self):
        return self.obj.body

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        self.replies_count = len(self.replies)
        super(Topic, self).save(*args, **kwargs)

    def get_reply_by_id(self, reply_id):
        try:
            return filter(lambda x: x.pk.hex == reply_id, self.replies)[0]
        except IndexError:
            return Post()

    def adjustRating(self, rating=0):
        Topic.objects.raw_update({"_id":ObjectId(self.pk)},{"$inc":{"rating":rating}})
        return self


#    def rate(self, rating, reply_id=None):
#        #self.rating += rating
#        Topic.objects.raw_update()
#        if reply_id:
#            self.get_reply_by_id(reply_id).rating += rating
#        return self.save()


    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'board_topic_view', (self.pk,), {}

    class Meta:
        ordering = ['-timestamp']