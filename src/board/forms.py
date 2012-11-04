from bson import ObjectId
from bson.errors import InvalidId
from django.contrib.auth.models import User

__author__ = 'pgcd'
from django.forms import ModelForm
from board.models import Post, Topic


class PostForm(ModelForm):
    def __init__(self, obj=None, user=None, *args, **kwargs):
        """Override the default to store the original document
        that comments are embedded in.
        """
        self.obj = obj
        super(PostForm, self).__init__(*args, **kwargs)

    def process_markup(self, markup):
        """
           This is where we'll do whatever markup processing we require.
        """
        return markup

    def clean(self):
        d = self.cleaned_data
        return d


    def save(self, *args):
        try:
            user = User.objects.get(pk=ObjectId(self.cleaned_data.get('user')))
        except (InvalidId, User.DoesNotExist):
            user = User(username='anon') #Maybe we can do better?

        self.instance.user = user
        self.instance.body = self.process_markup(self.instance.body_markup)

        if self.obj is None: #Starting a new topic!
            self.obj = Topic(obj=self.instance)
        else:
            self.obj.replies.add(self.instance)
        self.obj.save()
        return self.obj

    class Meta:
        model = Post
        fields = ['title','body_markup', 'user']

