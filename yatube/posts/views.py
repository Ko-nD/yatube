from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
from posts.models import Post, Group, User, Comment, Follow
from posts.forms import PostForm, CommentForm


def index(request):
    post_list = (
        Post.objects.select_related('author')
        .select_related('group')
        .order_by('-pub_date')
        .annotate(comment_count=Count('post_comment'))
    )

    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator, 'index_edit': True})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = (
        Post.objects.filter(group=group)
        .select_related('author')
        .order_by('-pub_date')
        .annotate(comment_count=Count('post_comment'))
    )
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "posts/group.html", {'group': group, 'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = 'Создание записи'
            text = 'Ваша запись была успешно опубликована!'
            return render(request, 'posts/post_success.html', {'title': title, 'text': text})
    title = 'Создать запись'
    button = 'Добавить'
    form = PostForm()
    return render(request, 'posts/post_new.html', {'form': form, 'title': title, 'button': button})


def profile(request, username, following=''):
    user_profile = get_object_or_404(User, username=username)
    post_list = (
        user_profile.author_posts.select_related('group')
        .order_by("-pub_date")
        .annotate(comment_count=Count('post_comment'))
    )

    paginator = Paginator(post_list, 10)
    posts_count = paginator.count
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    followers = Follow.objects.filter(author=user_profile).count()
    follows = Follow.objects.filter(user=user_profile).count()
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user, author=user_profile).all()
    context = {'user_profile': user_profile, 'page': page, 'paginator': paginator, \
        'posts_count': posts_count, 'following': following, 'follows': follows, 'followers': followers}
    return render(request, "posts/profile.html", context)


def post_view(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    posts_count = Post.objects.filter(author=user_profile).count()
    comments = post.post_comment.order_by("-created").all()
    followers = Follow.objects.filter(author=user_profile).count()
    follows = Follow.objects.filter(user=user_profile).count()
    form = CommentForm()
    context = {'user_profile': user_profile, 'post': post, 'posts_count': posts_count, \
        'comments': comments, 'follows': follows, 'followers': followers, 'form': form}
    return render(request, "posts/post.html", context)


@login_required
def post_edit(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                title = 'Редактирование записи'
                text = 'Ваша запись была успешно отредактирована!'
                return render(request, 'posts/post_success.html', {'title': title, 'text': text})
        title = 'Редактировать запись'
        button = 'Сохранить'
        form = PostForm()
        return render(request, 'posts/post_new.html', {'form': form, 'title': title, 'button': button})
    else:
        return redirect(reverse('post', args=[username, post_id]))


@login_required
def post_delete(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    if request.user == user_profile:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        title = 'Удаление записи'
        text = 'Ваша запись была успешно удалена!'
        return render(request, 'posts/post_success.html', {'title': title, 'text': text})
    else:
        return redirect(reverse('post', args=[username, post_id]))


@login_required
def add_comment(request, username, post_id):
    user_profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(reverse('post', args=[username, post_id]))
    form = CommentForm()
    return render(request, 'posts/comment.html', {'form': form})


@login_required
def follow_index(request):
    post_list = (
        Post.objects.filter(author__following__user=request.user)
        .select_related('author')
        .select_related('group')
        .order_by('-pub_date')
        .annotate(comment_count=Count('post_comment'))
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/follow.html', {'page': page, 'paginator': paginator, 'index_edit': True})


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=user, author=author).count()
    if user != author and not follow:
        Follow.objects.create(user=user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=user, author=author).count()
    if user != author and follow:
        Follow.objects.filter(user=user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
