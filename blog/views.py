from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView, FormView):
    queryset = Post.published.all()
    form_class = CommentForm
    template_name = 'blog/post/details.html'

    def get_success_url(self):
        obj = self.get_object()
        return reverse("blog:post_detail", kwargs={'slug': obj.slug })

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.active()
        return context

    def form_valid(self, form):
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)

