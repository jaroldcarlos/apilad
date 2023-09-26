from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from .models import Page, CategoryEvent, Event, Picture, Promotion


class PictureInline(admin.StackedInline):
    model = Picture
    verbose_name = _('Picture')
    verbose_name_plural = _('Gallery')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(CategoryEvent)
class CategoryEventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_at')
    list_display_links = ('title', )
    search_fields = ('title', )
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        PictureInline,
    ]
    fieldsets = (
        (_('STATUS'), {
            'fields': (
                'published_at',
                'expired_at',
                'status'
            ),
        }),
        (_('CONTENT'), {
            'fields': (
                'title',
                'slug',
                'description_short',
                'description',
                'ticket_purchase_link',
                'text_show_date',
                'text_show_geo',
                'link',
            ),
        }),
        (_('GEO'), {
            'fields': (
                'latitude',
                'longitude'
            ),
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_keywords',
                'meta_description'
            ),
        }),
        (_('IMAGE'), {
            'fields': (
                'image',
            ),
        }),
    )
    save_on_top = True

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    list_display_links = ('title', )
    search_fields = ('title', )