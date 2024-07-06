from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField as RichTextField
from sorl.thumbnail import ImageField
from meta.models import ModelMeta

from core.managers import InUseManager, IsApprovedManager
from core.abstract import SlugModel, PublishedModel, TimeStampedModel, ActiveModel

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

class Category(ActiveModel, SlugModel):
    name = models.CharField(_('name'), max_length=50, unique=True)

    objects = models.Manager()
    in_use = InUseManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Tag(ActiveModel, SlugModel):
    name = models.CharField(_('name'), max_length=50, unique=True)

    objects = models.Manager()
    in_use = InUseManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Author(ActiveModel, SlugModel):
    name = models.CharField(_('name'), max_length=255)

    objects = models.Manager()
    in_use = InUseManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Post(ActiveModel, SlugModel, PublishedModel, TimeStampedModel, ModelMeta):
    title = models.CharField(_('title'), max_length=255)
    subtitle = models.CharField(_('subtitle'), max_length=255, blank=True)

    excerpt = models.TextField(_('excerpt'),)
    text = RichTextField(_('text'),)

    featured = models.BooleanField(
        _('featured'),
        default=False,
        help_text=_('Display on the home page')
    )

    image = ImageField(
        _('imagen'),
        upload_to='blog_posts/',
        default='static/ecd_blog/images/default.png',
        blank=True
    )

    author = models.ForeignKey(
        Author,
        related_name='posts',
        verbose_name=_('autor'),
        on_delete=models.PROTECT
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='posts',
        verbose_name=_('tags'),
        blank=True
    )

    category = models.ForeignKey(
        Category,
        related_name='posts',
        verbose_name=_('category'),
        on_delete=models.PROTECT,
        blank=True
    )

    meta_title = models.TextField(_('meta-title'), max_length=55, default='', help_text=_('with a maximum of 55 characters'))
    meta_description = models.TextField(_('meta-description'), max_length=140, default='', help_text=_('with a maximum of 140 characters'))
    _metadata = {
        'title': 'meta_title',
        'description': 'meta_description',
        'image': 'get_meta_image'
    }

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def get_prev_post(self):
        return Post.published.filter(
            active=True,
            published_at__lt=self.published_at
        ).order_by(
            'published_at'
        ).last()

    def get_next_post(self):
        return Post.published.filter(
            active=True,
            published_at__gt=self.published_at
        ).order_by(
            'published_at'
        ).first()


    @property
    def list_of_approved_comments(self):
        objects = self.comments.all()
        objects = objects.filter(approved=True)
        return objects

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = _('new')
        verbose_name_plural = _('news')
        ordering = ['-published_at']


class Picture(models.Model):
    alt = models.CharField(_('alt'), max_length=255)
    image = ImageField(_('image'), upload_to='blog_galleries/')
    post = models.ForeignKey(
        Post,
        related_name='pictures',
        verbose_name=_('news'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.alt}'

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

class Comment(ActiveModel, TimeStampedModel):
    #user = models.ForeignKey(
    #    USER_MODEL,
    #    related_name='comments',
    #    verbose_name=_('user'),
    #    blank=True,
    #    null=True,
    #    on_delete=models.PROTECT
    #)
    text = models.TextField(_('text'),)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        verbose_name=_('news'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    approved = models.BooleanField(_('approved'), default=False)

    objects = models.Manager()
    is_approved = IsApprovedManager()
    # TODO eliminar approved y Is_aproved_manager para usar active que ya está

    # TODO que se muestre el contador en detalles y en los listados de solo los aprobados

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['approved', 'post', 'created_at']
