from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^/?$', login_required(views.BoardView.as_view()), name='board'),
    url(r'^(?P<pk>\d+)/?$', login_required(views.BoardTopicView.as_view()), name='board_topic'),
    url(r'^(?P<pk>\d+)/new/?$', views.TopicNewView.as_view(), name='new_topic')
]