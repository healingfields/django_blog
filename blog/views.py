from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published_posts.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'
# def post_list(request):
#     posts = Post.published_posts.all()
#     paginator = Paginator(posts, 3)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/post_list.html', {'page':page, 'posts':posts})

def post_detail(request, year, month, day,post_slug):
    post = get_object_or_404(Post, slug=post_slug,
                                    status='published',
                                    publish__year=2021,
                                    publish__month=11,
                                    publish__day=25)
    return render(request, 'blog/post/post_detail.html', {'post':post})
