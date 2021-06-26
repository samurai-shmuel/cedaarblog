from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django_email_verification import send_email
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import UpdateView, DeleteView
from .models import Posts, Comments, Category, User, Visitors
from .forms import CustomUserCreationForm, UserLoginForm, PostForm, CommentForm


def index(request):
    posts = Posts.objects.order_by('-timestamp')
    if len(posts) > 4:
        context = {
            'latest': posts[:4]
        }
    else:
        context = {
            'latest': posts
        }
    return render(request, 'index.html', context)


def paginate_query(queryset, pg):
    paginator = Paginator(queryset, 16)
    try:
        posts = paginator.page(pg)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def posts(request):
    categories = Category.objects.all()
    context = {}
    queryset = Posts.objects.all().order_by('-timestamp')
    page = request.GET.get('page')
    if request.GET.get("searched"):
        searched = request.GET.get("searched")
        queryset = queryset.filter(Q(subject__contains=searched) | Q(author_str__contains=searched))
    if request.POST.get("category"):
        recv = request.POST.get('category')
        category = Category.objects.get(name=recv)
        category.is_active = not category.is_active
        category.save()
        if category.is_active and category.name=='uncategorized':
            queryset = Posts.objects.filter(category=None).order_by('-timestamp')
        else:
            for item in categories:
                if item.is_active:
                    queryset = queryset.filter(category__name=item.name)
        context['posts'] = paginate_query(queryset, page)
    else:
        for item in categories:
            if item.is_active:
                item.is_active = False
    context['posts'] = paginate_query(queryset, page)
    context['categories'] = categories
    return render(request, 'posts.html', context)


def email_comment(obj):
    subject = f"Comment by {obj.commenter_str} to {obj.post}"
    message = '"' + obj.comment + '"'
    receiver = ['samtomann@gmail.com', 'cedaardesignstudio@gmail.com']
    if obj.post.author.email not in receiver:
        receiver.append(obj.post.author.email)
    sender_mail = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        sender_mail,
        receiver,
    )


def postview(request, pk):
    post = Posts.objects.get(id=pk)
    user = request.user
    form = CommentForm(request.POST or None)
    if form.is_valid():
        if user.is_authenticated:
            obj = form.save(commit=False)
            obj.post = post
            obj.commenter = User.objects.filter(email=user.email).first()
            obj.commenter_str = obj.commenter
            email_comment(obj)
            obj.save()
            return HttpResponseRedirect(reverse('postview', args=[str(pk)]))
        else:
            return redirect('login')
    liked_by = post.likes.filter(id=request.user.id).exists()
    if user == post.author or user.is_superuser:
        comments = Comments.objects.filter(post=post)
    elif user.is_active:
        comments = Comments.objects.filter(post=post, viewable=True) | Comments.objects.filter(post=post,
                                                                                               commenter=user)
    else:
        comments = Comments.objects.filter(post=post, viewable=True)

    def get_ip(request):
        adress = request.META.get('HTTP_X_FORWARDED_FOR')
        if adress:
            ip = adress.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    ip = get_ip(request)
    visitor = Visitors(user=ip, post=post)
    check = Visitors.objects.filter(user=ip).filter(post=post)
    if not check:
        visitor.save()
    visits = Visitors.objects.all()
    context = {"post": post, "comments": comments, "form": form, "liked": liked_by, "visits":visits}
    return render(request, 'blog.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        nexte = request.POST.get('next', '/')
        return HttpResponseRedirect(nexte)
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_active:
                login(request, user)
                nexte = request.POST.get('next', '/')
                if nexte == '/register/':
                    return redirect('index')
                return HttpResponseRedirect(nexte)
    else:
        form = UserLoginForm()
    context['loginform'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    nexte = request.GET.get('next', '/')
    return HttpResponseRedirect(nexte)


def register(request):
    context = {}
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            inac_user = User.objects.get(email=email)
            send_email(inac_user)
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = CustomUserCreationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


def confirm(request):
    context = {}
    return render(request, 'confotp.html', context)


# def again(request):
#     message = "Come"
#     if request.POST:
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(email=email, password=password)
#         if user:
#             inac_user = User.objects.get(email=email)
#             send_email(inac_user)
#             redirect('index')
#         else:
#             message = "Invalid Information"
#     context = {"message":message}
#     return render(request, 'confotp.html', context)


def email_post(pk):
    post = Posts.objects.get(pk=pk)
    context = {
        "post": post,
    }
    subject = f"{post.author} has uploaded a new post - {post.subject}"
    content = render_to_string('notification.html', context)
    message = strip_tags(content)
    receiver = [user.email for user in User.objects.filter(is_subscribed=True)]
    sender_mail = settings.EMAIL_HOST_USER
    email = EmailMultiAlternatives(
                subject,
                message,
                sender_mail,
                receiver,
            )
    email.attach_alternative(content, 'text/html')
    email.send()


def postcreate(request):
    context = {}
    form = PostForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.author_str = obj.author
        obj.save()
        category = form.clean_category()
        for item in category.iterator():
            obj.category.add(item)
        pk = obj.pk
        email_post(pk)
        return redirect('postview', pk=pk)
    context['form'] = form
    return render(request, "create.html", context)


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['subject', 'content', 'category', 'thumbnail']
    template_name = 'create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/posts/'
    template_name = 'delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Create your views here.
@login_required
def liker(request, pk):
    post = get_object_or_404(Posts, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('postview', args=[str(pk)]))


@login_required
def del_comment(request, pk, ck):
    comment = get_object_or_404(Comments, id=ck)
    if request.user.is_admin or comment.commenter == request.user:
        comment.delete()
    return HttpResponseRedirect(reverse('postview', args=[str(pk)]))


@login_required
def reveal(request, ck, pk):
    comment = get_object_or_404(Comments, id=ck)
    if request.user.is_admin:
        if comment.viewable:
            comment.viewable = False
        else:
            comment.viewable = True
        comment.save()
    return HttpResponseRedirect(reverse('postview', args=[str(pk)]))


@login_required
def subscribe(request):
    if request.POST:
        nexte = request.GET.get('next', '/')
        user = User.objects.get(id=request.user.id)
        user.is_subscribed = not user.is_subscribed
        user.save()
        return HttpResponseRedirect(nexte)
