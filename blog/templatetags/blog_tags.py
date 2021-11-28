from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import  mark_safe

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published_posts.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published_posts.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag()
def most_commented_posts(count=5):
    return Post.published_posts.annotate(total_comments = Count('comments')
                                         ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))



