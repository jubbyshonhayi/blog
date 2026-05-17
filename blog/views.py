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
from .models import Post, Comment


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

        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        parent = None

        # Determine who to tag
        if parent_id:
            parent = Comment.objects.select_related('user').get(id=parent_id)
            tagged_username = parent.user.username
        else:
            tagged_username = self.object.author.username

        # Auto-tag user
        content = f"@{tagged_username} {content}"

        Comment.objects.create(
            post=self.object,
            user=request.user,
            content=content,
            parent=parent
        )

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

