from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import MailForm, CommentForm
from django.core.mail import send_mail


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

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    post_comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog/post/post_detail.html', {'post': post,
                                                          'comments': post_comments,
                                                          'new_comment': new_comment,
                                                          'form': form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}'s comments : {cd['comments']}"
            print(cd)
            send_mail(subject, message, cd['email'], [cd['to']], fail_silently=True)
            sent = True
    else:
        form = MailForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
