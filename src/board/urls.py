from django.conf.urls.defaults import patterns, include, url
from board.views import PostDetailView, PostListView, TopicListView, TopicDetailView

urlpatterns = patterns('',
    url(r'^$', TopicListView.as_view(), name='board_topic_list'),
    url(r'^posts$', PostListView.as_view(), name='board_post_list'),
    url(r'^tag/(?P<tag>[\w\s]+)/$', TopicListView.as_view(), name='board_topic_list_by_tag'),
    url(r'^user/(?P<username>[^/]+)/posts$', PostListView.as_view(), name='board_post_list_by_user'),
    url(r'^user/(?P<username>[^/]+)/$', TopicListView.as_view(), name='board_topic_list_by_user'),
    url(r'^(?P<pk>\w+)/$', TopicDetailView.as_view(), name='board_topic_view'),
    url(r'^(?P<pk>\w+)/#(?P<post>\w+)$', TopicDetailView.as_view(), name='board_topic_view'),
)
