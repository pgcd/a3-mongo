import datetime
import random
from bson import ObjectId
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum
from django.db import models
from django.db.models import permalink, F
from djangotoolbox.fields import ListField, EmbeddedModelField, SetField
from uuidfield import UUIDField
# Create your models here.
import time
from django_mongodb_engine.contrib import MongoDBManager
from profiles.models import Profile
from tags.models import Tag


class PostManager(MongoDBManager):
    def createRubbish(self, topic=None):
        """
        :return: Post
        """
        p = Post(topic=topic)
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
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    body_markup = models.TextField(blank=True)
    summary = models.TextField(blank=True, default='')
    user = EmbeddedModelField(User, blank=True, null=True, db_index=True)
    deleted = models.BooleanField()
    hidden = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    topic = models.ForeignKey("Topic", blank=True, null=True, related_name="replies") #Nullable for first posts
    rating = models.IntegerField(default=0)

    ip = models.IPAddressField(default='0.0.0.0')

    objects = PostManager()

    def __unicode__(self):
        if self.title:
            return u"%s [#%s]" % (self.title, self.pk,)
        else:
            return u"#%s" % self.pk

    def adjustRating(self, rating=0):
        Post.objects.raw_update({"_id": ObjectId(self.pk)}, {"$inc": {"rating": rating}})
        self.topic.adjustRating(rating)
        return self

    def addToUserPosts(self):
        Profile.objects.raw_update(
            {"user_id": ObjectId(self.user.pk)},
            {"$addToSet": {"topics": self.topic_id}, })
        return self

    def save(self, force_insert=False, force_update=False, using=None):
        result = super(Post, self).save(force_insert, force_update, using)
        if self.topic is not None:
            self.topic.updateRepliesCount()
#            self.addToUserPosts() #The data transfer is massive so the benefit of this is slim to negative.
        return result

    class Meta:
        ordering = ['id']
        get_latest_by = 'id'

    @permalink
    def get_absolute_url(self):
        return 'board_topic_view', (), {'pk':self.topic_id, 'post':self.pk}

class TopicManager(MongoDBManager):
    def createRubbish(self, reply_chance=0.985):
        p = Post.objects.createRubbish()
        t = Topic(obj=p)
        for i in range(0, random.randint(0, 5)):
            t.tag(lorem_ipsum.words(random.randint(1, 2), False))
        if random.randint(0, 50) == 1:
            t.homepage = True
        t.deleted = p.deleted
        t.hidden = p.hidden
        t.save()
        while random.random() < reply_chance:
            t.replies.add(Post.objects.createRubbish())
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

class Topic(models.Model):
    homepage = models.BooleanField(db_index=True)
    hidden = models.BooleanField()
    deleted = models.BooleanField()
    tags = SetField(db_index=True)
    obj = EmbeddedModelField()
    objects = TopicManager()
    views_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)
    timeshift = models.IntegerField(default=0) #Mostly used for bookkeeping, but might be useful later
    timestamp = models.PositiveIntegerField(default=0, db_index=True)


    def __init__(self, *args, **kwargs):
        super(Topic, self).__init__(*args, **kwargs)


    @property
    def title(self):
        return self.obj.title or self.pk

    @property
    def body(self):
        return self.obj.body

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
#        self.addToUserTopics() #The data transfer is massive so the benefit of this is slim to negative.
        super(Topic, self).save(*args, **kwargs)


    def updateRepliesCount(self):
        replies_count = self.replies.count()
        Topic.objects.raw_update({"_id": ObjectId(self.pk)}, {"$set": {"replies_count": replies_count}})
        return replies_count

    def addToUserTopics(self):
        try:
            Profile.objects.raw_update(
                {"user_id": ObjectId(self.obj.user.pk)},
                {"$addToSet": {"topics": self.pk}, })
        except AttributeError:
            #If the obj has no user attribute (it's not a Post, for instance)
            pass
        return self

    def adjustRating(self, rating=0):
        Topic.objects.raw_update({"_id": ObjectId(self.pk)}, {"$inc": {"rating": rating}})
        return self

    def tag(self, tagname):
        self.tags.add(tagname)
        return Tag.objects.create_or_update_count(tagname, self)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'board_topic_view', (self.pk,), {}

    class Meta:
        ordering = ['-timestamp']