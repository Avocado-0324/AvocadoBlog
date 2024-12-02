from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db import models
from django.db.models import Count, Q, Max
from .models import Post, Category, Comment, Tag


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # 指定模板
    context_object_name = 'posts'  # 在模板中使用的变量名
    ordering = ['-created_date']  # 按创建时间倒序排列
    paginate_by = 10  # 每页显示10篇文章

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None)
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(ListView):
    model = Post
    template_name = 'blog/category_detail.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(categories__slug=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['category'])
        return context

def category_list(request):
    categories = Category.objects.annotate(post_count=Count('posts'))
    return render(request, 'blog/category_list.html', {'categories': categories})

def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        author = request.POST.get('author')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if author and content:
            comment = Comment.objects.create(
                post=post,
                author=author,
                content=content
            )
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
                comment.save()
                
    return redirect('blog:post_detail', pk=pk) 

class AboutView(TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_me'] = {
            'name': '阿波卡多',
            'bio': '热爱生活，记录成长。',
            'interests': ['编程', '写作', '育儿'],
            'social_links': {
                'github': 'https://github.com/yourusername',
                'email': 'your.email@example.com',
            }
        }
        return context 

def about(request):
    tags = Tag.objects.annotate(posts_count=Count('post')).filter(posts_count__gt=0)

    context = {
        'tags': tags,
    }
    return render(request, 'blog/about.html', context)