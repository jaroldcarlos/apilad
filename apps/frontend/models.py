from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.conf import settings
from meta.models import ModelMeta
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .function import presave_resize_image, presave_quality_image

from core.abstract import (
    AccesibilityModel,
    ActiveModel,
    BuyableModel,
    DescriptionModel,
    GeoModel,
    OptionsModel,
    TimeStampedModel,
    PublishedModel,
    SeoModel,
    SlugModel,
)

User = settings.AUTH_USER_MODEL

class CategoryEvent(ActiveModel, DescriptionModel, SeoModel, SlugModel):
    image = ImageField(
        _('image'),
        upload_to='category_event/',
        blank=True,
        null=True
    )
    title = models.CharField(
        _('title'),
        blank=True,
        max_length=200,
        default=""
    )

    class Meta:
        verbose_name = _('event category')
        verbose_name_plural = _('event categories')


class Page(ActiveModel, TimeStampedModel, ModelMeta):
    title = models.CharField(_('title'),max_length=255, blank=True, null=True)
    slug = models.SlugField(_('slug'), unique=True)
    image = ImageField(_('image'), upload_to='images/', blank=True, null=True)
    content = RichTextField(_('content'))
    publish_on = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        default= settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager('publish_on')

    meta_title = models.TextField(
        _('meta-title'),
        max_length=55, default='',
        help_text=_('con un máximo de 55 caracteres')
    )
    meta_description = models.TextField(
        _('meta-description'),
        max_length=140, default='',
        help_text=_('con un máximo de 140 caracteres')
    )
    _metadata = {
        'title': 'meta_title',
        'description': 'meta_description',
        'extra_props': {
            'designer': 'Pablo Picasso',
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0',
        },
        'extra_custom_props': 'get_custom_props',

    }

    def get_custom_props(self):
        return [
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8')
        ]

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
         return reverse('frontend:page', kwargs={'slug': self.slug})

    class Meta:
        unique_together = ['publish_on', 'slug']
        ordering = ['title']
        verbose_name = _('page')
        verbose_name_plural = _('pages')



class Event(
    AccesibilityModel,
    BuyableModel,
    DescriptionModel,
    GeoModel,
    SeoModel,
    ModelMeta,
    OptionsModel,
    PublishedModel,
):

    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_('creator'),
        related_name="events",
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        CategoryEvent,
        verbose_name=_('category'),
        related_name="events",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    title = models.CharField(
        _('title'),
        max_length=200,
    )

    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=200
    )
    image = ImageField(
        _('image'),
        upload_to='events/images/',
        blank=True,
        null=True
    )
    ticket_purchase_link = models.URLField(_('link de compra'), null=True, blank=True, help_text=_('Link para comprar la entrada al evento'))
    text_show_date = models.TextField(_('texto de Fecha'), blank=True, null=True, default='')
    text_show_geo = models.TextField(_('Texto de Lugar'), blank=True, null=True, default='')

    _metadata = {
        'title': 'title',
        'description': 'description_short',
        'image': 'get_meta_image'
    }

    def __str__(self):
        return '{}'.format(self.title)

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def get_absolute_url(self):
         return reverse('frontend:event_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('-published_at',)


class Picture(models.Model):
    alt = models.CharField(_('alt'), max_length=255)
    image = ImageField(_('image'), upload_to='blog_galleries/')
    event = models.ForeignKey(
        Event,
        related_name='pictures',
        verbose_name=_('event'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.alt


@receiver(pre_save, sender=Event)
def pre_save_slug_place(sender, instance, **kwargs):
    if instance.image:
        presave_resize_image(instance)

@receiver(pre_save, sender=Picture)
def pre_save_slug_place(sender, instance, **kwargs):
    if instance.image:
        presave_quality_image(instance)
