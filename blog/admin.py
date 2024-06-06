from django.contrib import admin
from .models import Post, Comment, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    ordering = ('status', 'created_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('text',)

def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Mark selected posts as published"


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)