from django.contrib import admin
from .models import Post, Category, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'display_categories')
    list_filter = ('created_date', 'categories')
    search_fields = ('title', 'content')
    filter_horizontal = ('categories', 'tags')
    fields = ['title', 'content', 'categories', 'tags', 'author']

    def display_categories(self, obj):
        """返回文章分类的列表显示"""
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = '分类'

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('content', 'author')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
