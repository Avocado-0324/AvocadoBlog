from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    categories = models.ManyToManyField('Category', verbose_name='分类', related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.CharField(max_length=100, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='父评论')
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.author}评论了{self.post.title}'
