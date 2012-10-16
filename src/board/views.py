# Create your views here.
from django.db.models.aggregates import Count
from django.views.generic import DetailView, ListView
from board.models import Post, Topic

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.djhtml'

class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.djhtml'
    paginate_by = 50


class TopicListView(ListView):
    model = Topic
    paginate_by = 50
    def get_queryset(self):
        qs = super(TopicListView, self).get_queryset()
        if 'username' in self.kwargs:
            qs = Topic.objects.raw_query({"replies.user.username":self.kwargs['username']})
        if 'homepage_only' in self.kwargs:
            qs = qs.filter(homepage=True)
        if 'tag' in self.kwargs:
            qs = qs.filter(tags=self.kwargs['tag'])
        return qs.order_by('-timestamp')
        #.annotate()[:50]

    def get_context_data(self, **kwargs):
        d =  super(TopicListView, self).get_context_data(**kwargs)
        d['request'] = self.request
        return d

class TopicDetailView(DetailView):
    model = Topic
    paginate_by = 50