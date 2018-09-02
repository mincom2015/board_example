# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from boards.models import Board, Post, Topic
from django.contrib.auth.models import User
from .forms import TopicNewForm


class BoardView(View):

    def get(self, request):
        boards = Board.objects.all()
        return render(request, 'board/index.html', {'boards': boards})


class BoardTopicView(View):

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        return render(request, 'board/topics.html', {'board': board})


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

            post = Post.objects.create(message=message, topic=topic, created_by=user)

            return redirect('board_topic', pk=board.pk)
        return render(request, 'board/topic_new.html', {'board': board, 'form': form})
