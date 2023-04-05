from django.utils.translation import gettext_lazy as _

from django.db import models

class Contact(models.Model):
    name = models.CharField(_('name'), max_length=120)
    email = models.EmailField(_('email'), max_length=150)
    telephone = models.CharField(_('telephone'), max_length=50)
    text = models.TextField(_('text'), max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
