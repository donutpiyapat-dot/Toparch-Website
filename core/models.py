from django.db import models
from django.utils.text import slugify
import uuid
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.html import format_html
import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from cloudinary.models import CloudinaryField

def unique_slugify(instance, slug_field, slug_from):
    slug = slugify(slug_from)
    ModelClass = instance.__class__

    unique_slug = slug
    counter = 1

    while ModelClass.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug

def project_image_path(instance, filename):
    """
    ใช้ได้ทั้ง Project.main_image และ ProjectImage.image
    """
    project = instance.project if hasattr(instance, 'project') else instance
    return f'projects/{project.slug}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')
    
STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),

    )

class Project(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    layout_type = models.CharField(
        max_length=50,
        choices=[
            ('grid', 'Grid'),
            ('hero', 'Hero'),
            ('masonry', 'Masonry'),
            ('split', 'Split Layout'),
            ('magazine', 'Magazine Layout'),
        ],
        default='grid'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects'
    )


    main_image = CloudinaryField(
        'image',
        transformation={
            "quality": "auto",
            "fetch_format": "auto"
        }
    )

    description = models.TextField(blank=True)
    area = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # search_vector = SearchVectorField(null=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug or "project"
            i = 1
            while Project.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title




class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='images',
        on_delete=models.CASCADE
    )

    image = CloudinaryField('image')

    image_type = models.CharField(
        max_length=10,
        choices=[('set1', 'Set 1'), ('set2', 'Set 2')],
        default='set1',
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']

    def preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="height:80px; border-radius:6px;" />',
                self.image.url
            )
        return "-"

    def __str__(self):
        return f"Image for {self.project.title}"



class ProjectDocument(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='documents',
        on_delete=models.CASCADE
    )
    document = models.FileField(upload_to='projects/documents/')
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="คำอธิบายเอกสารสั้นๆ"
    )

    def __str__(self):
        return f"Document for {self.project.title}"


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="ชื่อเอกสาร")
    file = models.FileField(upload_to='documents/', verbose_name="ไฟล์เอกสาร")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="รายละเอียดเพิ่มเติม"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="วันที่อัปโหลด"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = "Document"
        verbose_name_plural = "Documents"
