# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

def index(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'posts/form.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return redirect('index')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect('index')
