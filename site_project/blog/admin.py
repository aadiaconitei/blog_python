from django.contrib import admin
from .models import Category, Post, Comment

# Register your models here.
admin.site.register(Category)
# admin.site.register(Post)
# admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_tag', 'status', 'post_date')
    list_filter = ("status",)
    search_fields = ['title', 'body']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'body')


