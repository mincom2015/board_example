from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^/?$', login_required(views.BoardView.as_view()), name='board'),
    url(r'^(?P<pk>\d+)/?$', login_required(views.BoardTopicView.as_view()), name='board_topic'),
    url(r'^(?P<pk>\d+)/new/?$', login_required(views.TopicNewView.as_view()), name='new_topic'),
    url(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.TopicPostView.as_view(), name='topic_post'),
    url(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.ReplyTopicView.as_view(), name='reply_topic'),
    url(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_post')

]
