from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from meta.views import MetadataMixin
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Post, Category, Tag, Author, Picture, Comment

from .forms import CommentForm


class PostList(MetadataMixin, generic.ListView):
    queryset = Post.published.order_by('-published_at')
    template_name = 'blog/post_list.html'

    def get(self, *args, **kwargs):
        queryset = Post.published.order_by('-published_at')
        if not queryset:
            return redirect('frontend:home')
        return super(PostList, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug', None)
        author_slug = self.kwargs.get('author_slug', None)
        tag_slug = self.kwargs.get('tag_slug', None)
        search = self.request.GET.get('search', None)

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            context['filter_category'] = category
        if author_slug:
            author = Author.objects.get(slug=author_slug)
            context['filter_author'] = author
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            context['filter_tag'] = tag
        if search:
            context['search'] = search
        context['categories'] = Category.in_use.all()[:4]

        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        author_slug = self.kwargs.get('author_slug', None)
        tag_slug = self.kwargs.get('tag_slug', None)
        search = self.request.GET.get('search', None)

        objects = Post.published.all()
        if category_slug:
            objects = objects.filter(category__slug=category_slug)
        if author_slug:
            objects = objects.filter(author__slug=author_slug)
        if tag_slug:
            objects = objects.filter(tags__slug=tag_slug)
        if search:
            objects = objects.filter(title__icontains=search)

        return objects


class PostDetail(generic.edit.FormMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_initial(self):
        return {"post": self.get_object(), "user":self.request.user}

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        context['categories'] = Category.in_use.all()
        context['comments'] = Comment.is_approved.filter(post=self.object)

        try:
            next_post = self.object.get_next_post()
        except:
            next_post = None

        try:
            prev_post = self.object.get_prev_post()
        except:
            prev_post = None

        if prev_post:
            context['prev_post'] = prev_post

        if next_post:
            context['next_post'] = next_post

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _('Tu comentario ha sido enviado'))
        form.save()
        return super().form_valid(form)
