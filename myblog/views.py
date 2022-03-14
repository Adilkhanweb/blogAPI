import posixpath
from urllib.parse import urljoin

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, \
    DetailView, CreateView, UpdateView, DeleteView

from blog.settings import BASE_DIR
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, AddCategoryForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


# Create your views here.

# def home(request):
#     return render(request, 'home.html', {})


def MyPostsView(request, author):
    my_posts = Post.objects.filter(author=author).order_by('-id')
    return render(request, 'my_posts.html',
                  {'my_posts': my_posts})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' ')).order_by('-id')
    return render(request, 'category_posts.html',
                  {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


# def AddCommentView(request, pk):
#     if request.method == "POST":
#         # post = get_object_or_404(Post, id=request.POST.get('post_id'))
#         if request.POST.get('body'):
#             saveb = Comment()
#             saveb.body = request.POST.get('body')
#             saveb.save()
#         if request.POST.get('name'):
#             saven = Comment()
#             saven.name = request.POST.get('name')
#             saven.save()
#     return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))
#


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    # def get(self, request, *args, **kwargs):
    #     if request.method == "POST":
    #         # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    #         if request.POST.get('body'):
    #             saveb = Comment()
    #             saveb.body = request.POST.get('body')
    #             saveb.save()
    #         if request.POST.get('name'):
    #             saven = Comment()
    #             saven.name = request.POST.get('name')
    #             saven.save()

    def get_success_url(self):
        return reverse('article-detail', kwargs={'pk':str(self.kwargs['pk'])})


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class AddCategoryView(CreateView):
    model = Category
    form_class = AddCategoryForm
    success_url = reverse_lazy('add_post')

    def form_valid(self, form):
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


def UserLikedPostsView(request, user):
    global liked_posts
    if Post.objects.filter(likes=user).exists():
        liked_posts = Post.objects.filter(likes=user)
    else:
        liked_posts = None
    return render(request, 'user_liked_posts.html', {'liked_posts': liked_posts})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))
