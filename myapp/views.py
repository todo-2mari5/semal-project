from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, User, EventInfo
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(req):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(req, 'myapp/post_list.html', {"posts": posts})

def post_detail(req, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(req, 'myapp/post_detail.html',{'post': post})

@login_required
def post_new(req):
    if req.method == "POST":
        form = PostForm(req.POST, req.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.thumb = form.cleaned_data['thumb']
            post.save()
            return redirect('myapp:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(req, 'myapp/post_edit.html', {'form': form})

def post_edit(req, pk):
    post = get_object_or_404(Post, pk=pk)
    if req.method == "POST":
        form = PostForm(req.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.save()
            return redirect('myapp:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(req, 'myapp/post_edit.html', {'form': form})

def post_draft_list(req):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(req, 'myapp/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('myapp:post_detail', pk=pk)

def post_remove(req, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('myapp:post_list')
