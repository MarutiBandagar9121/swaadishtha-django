from django.db import models
from django.utils.text import slugify
import uuid
from .services.file_upload import get_product_image_upload_path, get_product_variant_image_upload_path


class Product(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    description = models.TextField(blank=True)
    # Many-to-Many with Category
    categories = models.ManyToManyField(
        'categories.Category',
        related_name='products',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            # slug already has a unique index from unique=True, but kept for explicitness
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            # common filter: active + published products
            models.Index(fields=['is_active', 'status']),
            # name search / ordering
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_product_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product Images'
        ordering = ['position']
        indexes = [
            # fetch images for a product in display order
            models.Index(fields=['product', 'position']),
        ]

    def __str__(self):
        return f"{self.product.name} — image {self.position}"


class Attribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Attributes"

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Attribute Values"
        # prevent duplicate values under the same attribute (e.g. two "Red" under Color)
        constraints = [
            models.UniqueConstraint(fields=['attribute', 'value'], name='unique_attribute_value')
        ]
        indexes = [
            models.Index(fields=['attribute', 'value']),
        ]

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    attribute_values = models.ManyToManyField('AttributeValue', related_name='variants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product Variants'
        indexes = [
            # most common query: get active variants for a product
            models.Index(fields=['product', 'is_active']),
            # sku already has a unique index, kept for explicitness
            models.Index(fields=['sku']),
            # price filtering on variants
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.product.name} — {self.sku}"


class VariantImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_product_variant_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Variant Images'
        ordering = ['position']
        indexes = [
            # fetch images for a variant in display order
            models.Index(fields=['variant', 'position']),
        ]

    def __str__(self):
        return f"{self.variant.sku} — image {self.position}"
