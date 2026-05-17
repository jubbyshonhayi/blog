from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .views import ( PostListView, 
                     PostDetailView, 
                     PostCreateView,
                     PostUpdateView,
                     PostDeleteView,
                     UserPostListView )
from . import views


def cache_public(view):
    return cache_page(60)(vary_on_cookie(view))


urlpatterns = [
    path('', cache_public(PostListView.as_view()), name='blog_home'),
    path('user/<str:username>/', cache_public(UserPostListView.as_view()), name='user-posts'),
    path('post/<int:pk>/', cache_public(PostDetailView.as_view()), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', cache_public(views.about), name='about'),
]
