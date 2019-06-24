from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(req):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    return render(req, 'myapp/post_list.html', {"posts":posts})
