from django.conf.urls.defaults import patterns, include, url
from board.views import PostDetailView, PostListView, TopicListView, TopicDetailView

urlpatterns = patterns('',
    url(r'^$', TopicListView.as_view(), name='board_topic_list'),
    url(r'^tag/(?P<tag>[\w\s]+)/$', TopicListView.as_view(), name='board_topic_list_by_tag'),
    url(r'^(?P<pk>\w+)/$', TopicDetailView.as_view(), name='board_topic_view'),
)
