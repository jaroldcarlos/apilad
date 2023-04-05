from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Picture, Post, Author, Tag, Category, Comment

from django.utils.translation import gettext_lazy as _

class PictureInline(admin.StackedInline):
    model = Picture
    verbose_name = _('Imagen')
    verbose_name_plural = _('Galería')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('featured', 'title', 'slug', 'category', 'tags_list', 'author', 'created_at', 'published_at')
    list_display_links = ('title',)

    list_filter = ('created_at', 'featured', 'category', 'author', 'tags')
    date_hierarchy = 'created_at'

    search_fields = ('title', 'slug', 'subtitle', 'excerpt', 'text' )

    readonly_fields = ('created_at', 'modified_at')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', )

    fieldsets = (
        (_('fechas'),
            {
                'fields': (
                    ('created_at', 'modified_at',),
                ),
            }
        ),
        (_('publicación'),
            {
                'fields': (
                    'featured',
                    'status',
                    ('published_at', 'expired_at'),
                ),
            }
        ),
        (_('datos'),
            {
                'fields': (
                    'author',
                    'category',
                    'image',
                ),
            }
        ),
        (_('Títulos'),
            {
                'fields': (
                    'title',
                    'slug',
                    'subtitle',
                ),
            }
        ),
        (_('textos'),
            {
                'fields': ('excerpt', 'text'),
            }
        ),
        (_('SEO'),
            {
                'fields': ('meta_title', 'meta_description'),
            }
        ),
        (_('etiquetas'),
            {
                'fields': (
                    'tags',
                ),
            }
        ),
    )
    inlines = [
        PictureInline,
    ]
    save_on_top = True

    @admin.display(description='Lista Etiquetas')
    def tags_list(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug' )

    search_fields = ('name', 'slug')

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Textos'),
            {
                'fields': (
                    'name',
                    'slug',
                ),
            }
        ),
    )



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

    search_fields = ('name', 'slug')

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Textos'),
            {
                'fields': (
                    'name',
                    'slug',
                ),
            }
        ),
    )



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

    search_fields = ('name', 'slug')

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Textos'),
            {
                'fields': (
                    'name',
                    'slug',
                ),
            }
        ),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'approved',
        'text',
        'post',
        #'user',
        'created_at',
        'buttons'
    )
    list_display_links = ('text', )

    # TODO eliminar filtro post en el futuro
    list_filter = ('created_at', 'post', )
    date_hierarchy = 'created_at'

    search_fields = ('text', )

    readonly_fields = ('created_at', 'modified_at')

    fieldsets = (
        (_('General'),
            {
                'fields': (
                    'approved',
                    'created_at',
                    #'user',
                    'post',
                ),
            }
        ),
        (_('Comentario'),
            {
                'fields': (
                    'text',
                ),
            }
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:comment_pk>/aprove', self.admin_site.admin_view(self.approve), name = 'blog_comment_approve'),
            path('<int:comment_pk>/remove', self.admin_site.admin_view(self.delete), name = 'blog_comment_remove'),
            ]
        return custom_urls + urls

    def approve(self, request, comment_pk):
        if comment_pk:
            comment = Comment.objects.get(pk=comment_pk)
            comment.approved = True
            comment.save()

            self.message_user(request, 'Comment {} Approved"'.format(comment.text), messages.SUCCESS)

        url = reverse(
            'admin:ecd_blog_comment_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

    def delete(self, request, comment_pk):
        if comment_pk:
            comment = Comment.objects.get(pk=comment_pk)
            comment.delete()

            self.message_user(request, 'Comment {} Deleted"'.format(comment.text), messages.SUCCESS)

        url = reverse(
            'admin:ecd_blog_comment_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

    def buttons(self, obj):
        aprobe_link = format_html(
            '<a class="addlink" href="{}">{}</a> ',
            reverse('admin:blog_comment_approve', args=[obj.pk]),
            _('publicar'),
        )
        delete_link = format_html(
            '<a class="deletelink" href="{}">{}</a>',
            reverse('admin:blog_comment_remove', args=[obj.pk]),
            _('eliminar'),
        )
        if obj.approved:
            return delete_link

        return delete_link + aprobe_link

    buttons.short_description = 'Opciones'
