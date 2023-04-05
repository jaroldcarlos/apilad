import re

from django.conf import settings
from django import template
from django.template import Node, TemplateSyntaxError

from ..models import Post, Category, Author, Tag

register = template.Library()

###########################################################
#     ____  _     ___   ____   _____  _    ____ ____      #
#    | __ )| |   / _ \ / ___| |_   _|/ \  / ___/ ___|     #
#    |  _ \| |  | | | | |  _    | | / _ \| |  _\___ \     #
#    | |_) | |__| |_| | |_| |   | |/ ___ \ |_| |___) |    #
#    |____/|_____\___/ \____|   |_/_/   \_\____|____/     #
#                                                         #
###########################################################

@register.inclusion_tag('blog/templatetags/blog_sidebar.html')
def blog_sidebar(search=None, categories=True, authors=True, tags=True):
    context = {
        'search':search,
        'categories':categories,
        'authors':authors,
        'tags':tags
    }
    return context

@register.inclusion_tag('blog/templatetags/blog_categories.html')
def blog_categories():
    categories = Category.in_use.all()
    return {
        'categories': categories
    }

@register.inclusion_tag('blog/templatetags/blog_authors.html')
def blog_authors():
    authors = Author.in_use.all()
    return {
        'authors': authors
    }

@register.inclusion_tag('blog/templatetags/blog_tags.html')
def blog_tags():
    tags = Tag.in_use.all()
    if tags:
        max_count = max(tag.posts_count for tag in tags)
    else:
        max_count = 0

    return {
        'tags': tags,
        'max_count': max_count
    }

@register.inclusion_tag('blog/templatetags/blog_search.html')
def blog_search(search=None):
    posts = Post.published.all()
    context = {
        'show':True if posts else False,
        'search':search
    }
    return context

@register.inclusion_tag('blog/templatetags/blog_menu.html')
def blog_menu():
    posts = Post.published.all()
    context = {
        'show':True if posts else False,
    }
    return context

@register.inclusion_tag('blog/templatetags/blog_featured.html')
def blog_featured(items=4, show_title=True, show_view_all=True, title=None):
    posts = Post.published.filter(featured=True)[:items]
    if not posts:
        posts = Post.published.all()
    return {
        'posts': posts,
        'show_title': show_title,
        'show_view_all': show_view_all,
        'title': title
    }
