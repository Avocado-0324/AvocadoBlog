from django.urls import path
from . import views
from .views import PostListView, PostDetailView, CategoryListView, CategoryDetailView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('about/', views.AboutView.as_view(), name='about'),
]