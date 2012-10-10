from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from board.views import PostListView, TopicListView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TopicListView.as_view(), {'homepage_only':True}, name='home'),
    url(r'^p/', include('board.urls')),
#    url(r'^t/', include('tags.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
