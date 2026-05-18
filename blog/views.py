from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from django.db.models import Prefetch
from .models import Post, Comment, Notification


MENTION_STRIP_CHARS = '.,:;!?()[]{}<>"\''


def extract_mentioned_usernames(content):
    usernames = set()

    for word in content.split():
        if not word.startswith('@') or len(word) == 1:
            continue

        username = word[1:].strip(MENTION_STRIP_CHARS)
        if username:
            usernames.add(username)

    return usernames


def create_comment_notifications(comment):
    recipients = {}

    if comment.parent_id and comment.parent.user_id != comment.user_id:
        recipients[comment.parent.user_id] = (
            comment.parent.user,
            f'{comment.user.username} replied to your comment.'
        )

    mentioned_usernames = extract_mentioned_usernames(comment.content)
    if mentioned_usernames:
        mentioned_users = User.objects.filter(username__in=mentioned_usernames)
        for mentioned_user in mentioned_users:
            if mentioned_user.id == comment.user_id:
                continue

            recipients.setdefault(
                mentioned_user.id,
                (
                    mentioned_user,
                    f'{comment.user.username} mentioned you in a comment.'
                )
            )

    notifications = [
        Notification(
            user=recipient,
            sender=comment.user,
            post=comment.post,
            comment=comment,
            message=message,
        )
        for recipient, message in recipients.values()
    ]

    if notifications:
        Notification.objects.bulk_create(notifications)


def blog_home(request):
    context = {'posts': Post.objects.select_related('author', 'author__profile')}
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related('author', 'author__profile').order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )
        return Post.objects.filter(
            author=user
        ).select_related('author', 'author__profile').order_by('-date_posted')


# =========================
# POST DETAIL + COMMENTS
# =========================
class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        replies = Comment.objects.select_related('user').order_by('date_posted')
        return Post.objects.select_related('author', 'author__profile').prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.select_related('user').order_by('-date_posted').prefetch_related(
                    Prefetch('replies', queryset=replies)
                ),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        comments = list(post.comments.all())

        # Only top-level comments
        context['comments'] = [
            comment
            for comment in comments
            if comment.parent_id is None
        ]
        context['comment_count'] = len(comments)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        parent = None

        if not content:
            return redirect(
                reverse(
                    'post-detail',
                    kwargs={'pk': self.object.pk}
                )
            )

        # Determine who to tag
        if parent_id:
            parent = Comment.objects.select_related('user').get(
                id=parent_id,
                post=self.object
            )
            tagged_username = parent.user.username
        else:
            tagged_username = self.object.author.username

        # Auto-tag user
        content = f"@{tagged_username} {content}"

        comment = Comment.objects.create(
            post=self.object,
            user=request.user,
            content=content,
            parent=parent
        )
        create_comment_notifications(comment)

        return redirect(
            reverse(
                'post-detail',
                kwargs={'pk': self.object.pk}
            )
        )


# =========================
# CREATE POST
# =========================
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# =========================
# UPDATE POST
# =========================
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# =========================
# DELETE POST
# =========================
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html')

