from .models import Post, User
from .forms import PostForm, LoginForm, UserCreateForm
from django.utils import timezone
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps

# Create your views here.
User = get_user_model()

# -------------- アプリ関連 --------------
def post_list(req):
    """投稿リスト"""
    posts = Post.objects.filter(event_date__gte=timezone.now(),published_date__lte=timezone.now()).order_by('-published_date')
    return render(req, 'myapp/post_list.html', {"posts": posts})

def post_detail(req, pk):
    """投稿の詳細"""
    post = get_object_or_404(Post, pk=pk)
    return render(req, 'myapp/post_detail.html',{'post': post})

@login_required
def post_new(req):
    """投稿画面"""
    if req.method == "POST":
        form = PostForm(req.POST, req.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.thumb = form.cleaned_data['thumb']
            post.flyer = form.cleaned_data['flyer']
            post.save()
            return redirect('myapp:post_draft', pk=post.pk)
    else:
        form = PostForm()
        return render(req, 'myapp/post_edit.html', {'form': form})

def post_draft(req, pk):
    """投稿確認"""
    post = get_object_or_404(Post, pk=pk)
    return render(req, 'myapp/post_draft.html', {'post': post})

def post_edit(req, pk):
    """投稿編集"""
    post = get_object_or_404(Post, pk=pk)
    if req.method == "POST":
        form = PostForm(req.POST, req.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = req.user
            post.thumb = form.cleaned_data['thumb']
            post.flyer = form.cleaned_data['flyer']
            post.save()
            return redirect('myapp:post_draft', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(req, 'myapp/post_edit.html', {'form': form})

def post_complete(req):
    """投稿完了"""
    return render(req, 'myapp/post_complete.html')

def post_archive(req):
    """アーカイブのリスト"""
    posts = Post.objects.filter(event_date__lt=timezone.now()).order_by('event_date')
    return render(req, 'myapp/post_archive.html', {'posts':posts})

def ajax_post_detail(req):
    pk = req.GET.get('pk')
    post = get_object_or_404(Post, pk=pk)
    d = {
        'title': post.title,
        'date': post.event_date,
        'img': post.thumb.url,
        'pdf': post.flyer.url,
        'venue': post.venue,
        'fee': post.fee,
        'regist': post.registration,
        'lang': post.lang,
        'host': post.host,
        'text': post.text,
    }
    return JsonResponse(d)

# -------------- アカウント関連 --------------
class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'registration/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'registration/logged_out.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'registration/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('registration/mail_template/create/subject.txt', context)
        message = render_to_string('registration/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('myapp:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'registration/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'registration/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()
