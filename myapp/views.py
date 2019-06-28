from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, User, EventInfo
from .forms import PostForm, EventForm
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
        post_form = PostForm(req.POST, req.FILES)
        event_form = EventForm(req.POST, req.FILES)
        if event_form.is_valid():
            event_info = event_form.save(commit=False)
            event_info.flyer = event_form.cleaned_data['flyer']
            event_info.save()
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = req.user
                post.thumb = post_form.cleaned_data['thumb']
                post.event = event_info
                post.save()
                return redirect('myapp:post_detail', pk=post.pk)
    else:
        post_form = PostForm()
        event_form = EventForm()
    return render(req, 'myapp/post_edit.html', {'post_form': post_form, 'event_form': event_form})

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
