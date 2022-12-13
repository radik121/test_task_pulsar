import os
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    class Status(models.TextChoices):
        IN_STOCK = 'in stock', _('in stock')
        ON_ORDER = 'on order', _('on order')
        RECEIPT_EXPECTED = 'receipt expected', _('receipt expected')
        NOT_AVAILABLE = 'not available', _('not available')
        NOT_PRODUCED = 'not produced', _('not produced')

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    price = models.DecimalField(_('price'), max_digits=15, decimal_places=2, default=0)
    status = models.CharField(_('status'), choices=Status.choices, default=Status.ON_ORDER, max_length=20)
    image = models.ImageField(_('image'), upload_to='images/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        name = str(self.image).split('.')
        if name[-1] in ['png', 'jpg']:
            image = Image.open(self.image.path).convert("RGB")
            path, _ = os.path.splitext(self.image.path)
            image.save(f'{path}.webp')

    def image_formats(self):
        filename, _ = os.path.splitext(self.image.path)
        filename = filename.split('/images/')[-1]
        extensions = set([file.split('.')[-1]
                         for file in os.listdir(f'{settings.MEDIA_ROOT}/images/')
                         if file.startswith(filename)])
        return extensions

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)

    property_objects = models.ManyToManyField(verbose_name=_('properties'), to='PropertyObject')

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(_('value type'), max_length=10, choices=Type.choices)

    def __str__(self):
        return f'{self.title} ({self.get_value_type_display()})'


class PropertyValue(models.Model):
    class Meta:
        verbose_name = _('property value')
        verbose_name_plural = _('properties values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(to=PropertyObject, on_delete=models.PROTECT)

    value_string = models.CharField(_('value string'), max_length=255, blank=True, null=True)
    value_decimal = models.DecimalField(_('value decimal'), max_digits=11, decimal_places=2, blank=True, null=True)
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product, related_name='properties')

    def __str__(self):
        return str(getattr(self, f'value_{self.property_object.value_type}', None))
