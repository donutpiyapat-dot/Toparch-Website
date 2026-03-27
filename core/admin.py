from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User, Group
from .models import Project, ProjectImage, ProjectDocument, Document, Category
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils.timezone import now
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import Project,ProjectImage, ProjectDocument
# ==============================
# INLINES
# ==============================

class ProjectImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProjectImage
    ordering = ('order',)
    extra = 0
    readonly_fields = ('image_preview',)
    fields = ('image','image_preview', 'order', 'alt_text')
    verbose_name = "Project Images (Set 1)"
    verbose_name_plural = "Project Images (Set 1)"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(image_type='set1')

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        obj.image_type = 'set1'
        if commit:
            obj.save()
        return obj
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px; border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Preview"


class SecondaryProjectImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProjectImage
    ordering = ('order',)
    extra = 0
    fields = ('image','image_preview', 'order', 'alt_text')
    readonly_fields = ('image_preview',)
    verbose_name = "Project Images (Set 2)"
    verbose_name_plural = "Project Images (Set 2)"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(image_type='set2')

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        obj.image_type = 'set2'
        if commit:
            obj.save()
        return obj
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px; border-radius:6px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Preview"


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1
    fields = ['document', 'description']


# ==============================
# PROJECT ADMIN
# ==============================

@admin.register(Project)
class ProjectAdmin(SortableAdminBase, admin.ModelAdmin):

    # ---- PERFORMANCE ----
    list_select_related = ('category',)

    # ---- LIST PAGE ----
    list_display = (
        'title',
        'category',
        'colored_status',
        'year',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
        'year',
    )

    search_fields = (
        'title',
        'slug',
        'description',
    )

    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 15

    actions = ['make_published']

    # ---- FORM PAGE ----
    inlines = [
        ProjectImageInline,
        SecondaryProjectImageInline,
        ProjectDocumentInline
    ]

    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = (
        'created_at',
        'updated_at',
        'main_image_preview',
    )

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
                'category',
                'main_image',
                'main_image_preview',
                'description'
            )
        }),
        ('Project Info', {
            'fields': ('area', 'year', 'status', 'layout_type')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # ---- CUSTOM DISPLAY ----

    def colored_status(self, obj):
        color_map = {
            'draft': 'gray',
            'published': 'green',
            'archived': 'red',
        }
        color = color_map.get(obj.status, 'black')

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            obj.status.upper()
        )

    colored_status.short_description = 'Status'

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height:120px; border-radius:8px;" />',
                obj.main_image.url
            )
        return "No Image"

    main_image_preview.short_description = 'Preview'

    # ---- BULK ACTION ----

    def make_published(self, request, queryset):
        queryset.update(status='published')

    make_published.short_description = "Mark selected as Published"


# ==============================
# CATEGORY ADMIN
# ==============================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}


# ==============================
# DOCUMENT ADMIN
# ==============================

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)


# ==============================
# CUSTOM ADMIN SITE
# ==============================
class CustomAdminSite(admin.AdminSite):
    site_header = "Toparch Admin"
    site_title = "Toparch Dashboard"
    index_title = "Dashboard Overview"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        total_projects = Project.objects.count()
        published = Project.objects.filter(status='published').count()
        draft = Project.objects.filter(status='draft').count()
        archived = Project.objects.filter(status='archived').count()
        total_categories = Category.objects.count()

        latest_projects = Project.objects.order_by('-created_at')[:5]

        projects_per_year = (
            Project.objects.values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        extra_context.update({
            'total_projects': total_projects,
            'published': published,
            'draft': draft,
            'archived': archived,
            'total_categories': total_categories,
            'latest_projects': latest_projects,
            'projects_per_year': projects_per_year,
        })

        return super().index(request, extra_context)


admin_site = CustomAdminSite(name='custom_admin')
admin_site.register(Project, ProjectAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(User)
admin_site.register(Group)