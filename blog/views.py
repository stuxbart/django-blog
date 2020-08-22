from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    queryset = Post.published.all()
    template_name = 'blog/post/details.html'
