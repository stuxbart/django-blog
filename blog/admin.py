from django.contrib import admin
from .models import Post, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    search_fields = ('name', 'body')
    list_filter = ('active', 'created')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post)
