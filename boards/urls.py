from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^/?$', views.BoardView.as_view(), name='board'),
    url(r'^(?P<pk>\d+)/?$', views.BoardTopicView.as_view(), name='board_topic'),
    url(r'^(?P<pk>\d+)/new/?$', views.TopicNewView.as_view(), name='new_topic')
]