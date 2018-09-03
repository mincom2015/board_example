# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View, UpdateView, ListView
from boards.models import Board, Post, Topic
from django.contrib.auth.models import User
from .forms import TopicNewForm, PostForm
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


class BoardView(View):
    def get(self, request):
        boards = Board.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(boards, 5)
        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
            boards = paginator.page(1)
        except EmptyPage:
            boards = paginator.page(paginator.num_pages)

        return render(request, 'board/index.html', {'boards': boards})


class BoardTopicView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'board/topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super(BoardTopicView, self).get_context_data(**kwargs)


    def get_queryset(self):
        self.board = Board.objects.get(pk=self.kwargs.get('pk'))

        topics = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return topics


class TopicNewView(View):
    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        form = TopicNewForm()
        return render(request, 'board/topic_new.html', {'board': board, 'form': form})

    def post(self, request, pk):
        board = Board.objects.get(pk=pk)
        form = TopicNewForm(request.POST)
        if form.is_valid():
            user = User.objects.filter().first()

            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            message = form.cleaned_data.get('message')

            Post.objects.create(message=message, topic=topic, created_by=user)
            return redirect('topic_post', pk=board.pk, topic_pk=topic.pk)
        return render(request, 'board/topic_new.html', {'board': board, 'form': form})


class TopicPostView(View):

    def get(self, request, pk, topic_pk):
        topic = Topic.objects.get(pk=topic_pk)
        session_key = 'viewed_topic_{}'.format(topic.pk)
        if not self.request.session.get(session_key, False):
            topic.views += 1
            topic.save()
            self.request.session[session_key] = True

        return render(request, 'board/topic_post.html', {'topic': topic})


class ReplyTopicView(View):
    def get(self, request, pk, topic_pk):
        topic = Topic.objects.get(pk=topic_pk)
        form = PostForm()
        return render(request, 'board/reply_post.html', {'topic': topic, 'form': form})

    def post(self, request, pk, topic_pk):
        topic = Topic.objects.get(pk=topic_pk)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            return redirect('topic_post', pk=pk, topic_pk=topic_pk)
        return render(request, 'board/reply_post.html', {'topic': topic, 'form': form})


class PostUpdateView(View):

    def get(self, request, pk, topic_pk, post_pk):
        post = Post.objects.get(pk=post_pk)
        form = PostForm(instance=post)
        return render(request, 'board/edit_post.html', {'post': post, 'form': form})

    def post(self, request, pk, topic_pk, post_pk):
        post = Post.objects.get(pk=post_pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('topic_post', pk=pk, topic_pk=topic_pk)
        return render(request, 'board/edit_post.html', {'post': post, 'form': form})
