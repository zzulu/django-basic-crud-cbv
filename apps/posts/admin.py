from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user','content',]}),
    ]
    inlines = [CommentInline]
    list_display = ('content','user','created_at','updated_at',)


admin.site.register(Post, PostAdmin)

