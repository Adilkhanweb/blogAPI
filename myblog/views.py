from django.shortcuts import render
from django.views.generic import ListView, \
    DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, EditForm
from django.urls import reverse_lazy


# ListView brings back list of posts
# DetailView brings back details of on post

# Create your views here.

# def home(request):
#     return render(request, 'home.html', {})

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-id']


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    # fields = '__all__'


class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
