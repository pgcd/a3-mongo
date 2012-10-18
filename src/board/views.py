# Create your views here.
from django.db.models.aggregates import Count
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import ProcessFormView, ModelFormMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from board.models import Post, Topic
from board.forms import PostForm

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
    form_class = PostForm

    def get_queryset(self):
        qs = super(TopicListView, self).get_queryset()
        if 'username' in self.kwargs:
            qs = Topic.objects.raw_query({"replies.user.username": self.kwargs['username']})
        if 'homepage_only' in self.kwargs:
            qs = qs.filter(homepage=True)
        if 'tag' in self.kwargs:
            qs = qs.filter(tags=self.kwargs['tag'])
        return qs.order_by('-timestamp')
        #.annotate()[:50]

    def get_context_data(self, **kwargs):
        d = super(TopicListView, self).get_context_data(**kwargs)
        d['request'] = self.request
        d['form'] = self.get_form(self.form_class)
        return d

    def get_form(self, form_class):
        return form_class(initial={'user': self.request.user})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            self.object = form.save()
            return redirect(self.object)
        return self.get(request, *args, **kwargs)


class TopicDetailView(DetailView):
    model = Topic
    paginate_by = 50

    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostForm(obj=self.object, initial={'user': request.user})
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostForm(obj=self.object, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(self.object)

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

