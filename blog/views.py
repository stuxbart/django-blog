from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from taggit.models import Tag
from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    template_name = 'blog/post/list.html'

    # def get_queryset(self):
    #     tag_slug = self.kwargs.get('slug') or None
    #     if tag_slug is not None:
    #         tag = get_object_or_404(Tag, slug=tag_slug)
    #         return Post.published.filter(tags__in=[tag])
    #     return Post.published.all()

    def get_context_data(self, *args, **kwargs):
        tag_slug = self.kwargs.get('slug') or None
        tag = None
        if tag_slug is not None:
            tag = get_object_or_404(Tag, slug=tag_slug)

            qs = Post.published.filter(tags__in=[tag])
        else:
            qs = Post.published.all()
        context = super(PostListView, self).get_context_data(object_list=qs)
        context['tag'] = tag
        return context


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

        tags_ids = context['object'].tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=tags_ids).exclude(id=context['object'].id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')

        context['similar_posts'] = similar_posts
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
