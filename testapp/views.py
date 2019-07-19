from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from django.http import JsonResponse


def post_lists(request):
    posts = Post.objects.all()
    return render(request, 'testapp/post_lists.html', {'posts':posts})

def ajax_post_add(request):
    title = request.POST.get('title')
    date = request.POST.get('date')
    post = Post.objects.create(title=title, date=date)
    d = {
        'title': 'hogehoge',
        'date': post.date,
    }
    return JsonResponse(d)

def ajax_post_detail(request):
    pk = request.GET.get('pk')
    post = get_object_or_404(Post, pk=pk)
    d = {
        'title': post.title,
        'date': post.date,
    }
    return JsonResponse(d)