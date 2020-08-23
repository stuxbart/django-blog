from django.urls import path

from .views import PostListView, PostDetailView, HideCommentView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('<slug>', PostDetailView.as_view(), name="post_detail"),
    path('hide/<int:pk>', HideCommentView.as_view(), name="comment_hide")
]
