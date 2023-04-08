from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from .managers import ActiveManager, PublishedManager, ReadOnlyManager


class ActiveModel(models.Model):
    """
    An abstract base class model that provides
    ``active`` field and a manager class.
    """
    active = models.BooleanField(
        _('active'),
        default=True
    )

    objects = models.Manager()
    actives = ActiveManager()

    class Meta:
        abstract = True


class AccesibilityModel(models.Model):
    a11y_accesss = models.BooleanField(_('access'), default=False)
    a11y_wc = models.BooleanField(_('wc'), default=False)
    a11y_info = models.BooleanField(_('information'), default=False)
    a11y_service = models.BooleanField(_('accesibility full'), default=False)
    a11y_text = models.TextField(_('aclarations'), null=True, blank=True, default="")

    class Meta:
        abstract = True


class BuyableModel(models.Model):

    min_age = models.CharField(_('min age'), blank=True, max_length=120)
    max_age = models.CharField(_('max age'), blank=True, max_length=120)

    requirements = models.TextField(
        _('requirements'),
        blank=True,
        null=True
        )
    price = models.DecimalField(_('price'), max_digits=5, decimal_places=2, blank=True, null=True)
    link = models.CharField(_('link'), blank=True, null=True, max_length=255)

    @property
    def free(self):
        return True if self.price == 0 else False

    class Meta:
        abstract = True


class CapacityModel(models.Model):
    min_people = models.CharField(
        _('min people'),
        blank=True,
        null=True,
        max_length=120
    )
    max_people = models.CharField(
        _('max people'),
        blank=True,
        null=True,
        max_length=120
    )

    class Meta:
        abstract = True


class DescriptionModel(models.Model):
    description_short = models.TextField(
        _('description short'),
        blank=True
    )
    description = RichTextField(
        _('description'),
        blank=True
    )

    def get_description_short(self, num_chars=245):
        if self.description_short:
            if len(self.description_short) > num_chars:
                return self.description_short[:num_chars] + '...'
            else:
                return self.description_short
        else:
            if len(self.description) > num_chars:
                return self.description[:num_chars] + '...'
            else:
                return self.description

    class Meta:
        abstract = True


class GeoModel(models.Model):
    latitude = models.CharField(_('latitude'), blank=True, max_length=40)
    longitude = models.CharField(_('longitude'), blank=True, max_length=40)

    def coordinates(self):
        return '{latitude}, {longitude}'.format(
            latitude=self.latitude,
            longitude=self.longitude
        )

    class Meta:
        abstract = True


class OptionsModel(models.Model):
    starred = models.BooleanField(_('starred'), default=False)
    child = models.BooleanField(_('child'), default=False)
    limited_seating = models.BooleanField(_('limited seating'), default=False)
    registration_required = models.BooleanField(_('registration required'), default=False)

    class Meta:
        abstract = True


class SeoModel(models.Model):
    meta_title = models.TextField(
        _('meta_title'),
        max_length=65,
        help_text=_('máximo de 65 carácteres, obligatorio para el SEO')
    )
    meta_keywords = models.TextField(
        _('meta_keywords'),
        help_text=_("lista de palabras o frases claves, entre comillas simples y separados por una coma (,). Ejemplo: 'APILAD', 'Evento Público', 'etc'"),
        null=True,
        blank=True
    )
    meta_description = models.TextField(
        _('meta_description'),
        help_text=_('entre de 120 a 330 carácteres, Obligatorio para el SEO')
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(_('slug'), unique=True, null=True, max_length=200)

    class Meta:
        abstract = True


class PublishedModel(models.Model):
    """
    An abstract base class model that provides a manager and
    ``published_at`` and ``expired_at`` fields.
    """
    class Status(models.TextChoices):
        FINISHED = 'f', _('Finished')
        ONHOLD = 'o', _('On hold')
        PUBLISHED = 'p', _('Published')
        DRAFT = 'd', _('Draft')

    published_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        _('Publication status'),
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()

    @property
    def is_published(self):
        if self.status != self.Status.PUBLISHED:
            return False

        if (self.published_at is not None and self.published_at > timezone.now()):
            return False

        if (self.expired_at is not None and self.expired_at < timezone.now()):
            return False

        return True


    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created_at`` and ``modified_at`` fields.
    """
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        abstract = True


class ReadOnlyModel(models.Model):
    """
    An abstract base class model that provides the ReadOnly manager.
    """
    objects = ReadOnlyManager()

    def save(self, *args, **kwargs):
        pass
        # raise NotImplemented

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        managed = False
        abstract = True


class ModelIterable(models.Model):
    """
    An abstract base class model that which displays the fields of the model
    """
    def __iter__(self):
        field_names = [f.name for f in self._meta.fields]
        for field_name in field_names:
            value = getattr(self, field_name, None)
            yield (field_name, value)

    def show(self):
        for f in self:
            print(f)

    class Meta:
        abstract = True


class GeoModel(models.Model):
    """
    An abstract base class model that provides geolocation fields.
    ``latitude`` and ``longitude`` fields.
    """
    latitude = models.DecimalField(
        _('latitude'),
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True
    )
    # location = models.PointField()

    class Meta:
        abstract = True


class AddressModel(models.Model):
    """
    An abstract base class model that provides contacts fields
    ``address``, ``state``.``city``and ``longitude`` fields.
    """
    address = models.CharField(
        _('address'),
        max_length=200,
        blank=True,
        null=True
    )
    state = models.CharField(
        _('state'),
        max_length=100,
        blank=True,
        null=True
    )
    city = models.CharField(
        _('city'),
        max_length=100,
        blank=True,
        null=True
    )
    cp = models.CharField(
        _('postal code'),
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
