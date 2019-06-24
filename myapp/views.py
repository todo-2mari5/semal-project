from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(req):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    return render(req, 'myapp/post_list.html', {"posts": posts})

def post_detail(req, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(req, 'myapp/post_detail.html',{'post': post})

def post_new(req):
    if req.method == "POST":
        form = PostForm(req.POST, req.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myapp/post_edit.html', {'form': form})
