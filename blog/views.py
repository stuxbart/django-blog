from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return reverse("blog:post_detail", kwargs={'slug': obj.slug})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            context['comments'] = self.get_object().comments.all()
        else:
            context['comments'] = self.get_object().comments.active()
        return context

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.save()
        return super(PostDetailView, self).form_valid(form)


class HideCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('pk') or None
        if comment_id is not None:
            comment = Comment.objects.get(pk=comment_id)

            if request.user.is_staff:
                comment.active = not comment.active
                comment.save()
            post_slug = comment.post.slug
            return redirect(reverse('blog:post_detail', kwargs={'slug': post_slug}))
        else:
            return redirect(reverse('blog:post_list'))
