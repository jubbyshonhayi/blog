from django.core.cache import cache

from .models import Post


def sidebar_posts(request):
    posts = cache.get('sidebar_latest_posts')
    if posts is None:
        posts = list(
            Post.objects.only('id', 'title', 'date_posted').order_by('-date_posted')[:5]
        )
        cache.set('sidebar_latest_posts', posts, 300)

    return {'latest_sidebar_posts': posts}
