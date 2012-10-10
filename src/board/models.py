import datetime
import random
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum
from django.db import models
from django.db.models import permalink
from djangotoolbox.fields import ListField, EmbeddedModelField
# Create your models here.
import time
from django_mongodb_engine.contrib import MongoDBManager

class PostManager(MongoDBManager):
    def createRubbish(self, topic):
        p = Post()
        p.topic = topic
        p.title = lorem_ipsum.words(random.randint(0, 5), False)
        p.body = p.body_markup = "<br/>\n".join(lorem_ipsum.paragraphs(random.randint(0,7), False))
        p.summary = lorem_ipsum.paragraph()
        p.user = User.objects.all()[random.randint(0,850)]
        if random.randint(1,50)==1:
            p.hidden = True
        if random.randint(1,100)==1:
            p.deleted = True

        p.save()
        return p



class Post(models.Model):
    #Data
    topic = models.ForeignKey('Topic', related_name="replies")
    title = models.CharField(max_length = 255, blank = True)
    body = models.TextField()
    body_markup = models.TextField(blank = True)
    summary = models.TextField(blank = True, default = '')
    user = EmbeddedModelField(User, blank=True, null=True, db_index=True)
    user_signature = models.TextField(blank = True, default = '')
    user_info = models.CharField(max_length = 255, blank = True, default = '')

    #Stats
#    user = models.ForeignKey(User, related_name = 'posts', blank = True, null = True)

    deleted = models.BooleanField()
    hidden = models.BooleanField()

#    content_type = models.ForeignKey(ContentType, blank = True, null = True)
#    object_id = models.PositiveIntegerField(blank = True, null = True, db_index = True)
#    in_reply_to = generic.GenericForeignKey()

    last_updated = models.DateTimeField(auto_now=True, null=True)

#    last_post = models.ForeignKey('self', related_name='last_reply_to', blank=True, null=True)
#    last_poster = models.ForeignKey(User, related_name='unanswered_replies', blank=True, null=True)
    #

    rating = models.IntegerField(default = 0)

    ip = models.IPAddressField(default = '0.0.0.0')
    #Denorm
    views_count = models.PositiveIntegerField(default = 0)
#    mentions = models.ManyToManyField(User, related_name = 'mentions', blank = True, null = True)
#    recipients = models.ManyToManyField(User, related_name='private_messages', blank=True, null=True)

    objects = PostManager()

    def __unicode__(self):
        if self.title:
            return u"%s [#%s]" % (self.title,self.pk,)
        else:
            return u"#%s" % self.pk

#    @permalink
#    def get_absolute_url(self):
#        return 'board_post_view', (self.pk,), {}


class TopicManager(MongoDBManager):
    def createRubbish(self, max_posts=3000):
        t = Topic()
        for i in range(0, random.randint(0, 5)):
            t.tags.append(lorem_ipsum.words(random.randint(1, 2), False))
        if random.randint(0,50)==1:
            t.homepage = True
        t.save()
        first = Post.objects.createRubbish(t)
        t.replies.add(first)
        t.title = first.title + '//'+t.pk
        t.body = first.body

        for i in range(0, random.randint(1, max_posts)):
            t.replies.add(Post.objects.createRubbish(t))

        return t



class Topic(models.Model):
    homepage = models.BooleanField(db_index=True)
    tags = ListField()
    #replies = ListField(EmbeddedModelField(Post))
    objects = TopicManager()
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)

    timeshift = models.IntegerField(default = 0) #Mostly used for bookkeeping, but might be useful later
    timestamp = models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        super(Topic, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'board_topic_view', (self.pk,), {}