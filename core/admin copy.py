from django.contrib import admin
from .models import Project, ProjectImage, ProjectDocument, Document , Category
# 1. ส่วนของ Gallery (รูปภาพหลายรูป)
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3  # จำนวนช่องว่างสำหรับอัปโหลดรูปที่เตรียมไว้ให้
    fields = ['image', 'caption']

# 2. ส่วนของเอกสารประกอบโปรเจกต์ (เช่น PDF แบบแปลน)
class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1  # เตรียมช่องว่างไว้ให้ 1 ช่องสำหรับแนบไฟล์
    fields = ['document', 'description']

# --- Custom Actions ---
@admin.action(description="Publish selected projects")
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)

@admin.action(description="Unpublish selected projects")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)

@admin.action(description="Mark as featured")
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)

@admin.action(description="Remove from featured")
def remove_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)

@admin.action(description="Mark as Completed")
def mark_completed(modeladmin, request, queryset):
    # แก้ไขให้ตรงกับ Choices ใน Model (ปกติ Django จะเก็บค่าตัวพิมพ์ใหญ่ตามที่ตั้งไว้)
    queryset.update(status="Completed") 

# 3. จัดการส่วนของ Project (หัวใจหลัก)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # รวมทั้งรูปภาพและเอกสารมาไว้ในหน้าเดียวกัน
    inlines = [ProjectImageInline, ProjectDocumentInline]
    # ตารางรวม (หน้าแรกของ Admin)
    list_display = (
        'title',
        'category',
        'status',
        'year',
        'is_published',
        'is_featured',
    )

    list_editable = (
        'status',
        'is_published',
        'is_featured',
    )

    list_filter = (
        'category',
        'status',
        'year',
        'is_published',
        'is_featured',
    )

    search_fields = ('title',)

    # การจัดกลุ่มหน้าแก้ไขข้อมูล (Fieldsets)
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'category',
                'status',
                'main_image',
                'description',
            )
        }),
        ('Project Info & Marketing', {
            'fields': (
                'area',
                'year',
                'is_published',
                'is_featured',
            )
        }),
    )

    actions = [
        make_published,
        make_unpublished,
        make_featured,
        remove_featured,
        mark_completed,
    ]
@admin.register(Category)
class CategoryAdmin(admin.


ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}

# 4. จัดการส่วนของ Document ทั่วไปของบริษัท (เช่น ใบเสนอราคา/แคตตาล็อกกลาง)
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)