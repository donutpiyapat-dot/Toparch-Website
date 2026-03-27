from core.admin import admin_site
from django.urls import path
from core import views 
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# รวมทุกอย่างไว้ในรายการเดียว ห้ามประกาศซ้ำ
urlpatterns = [
    path('admin/', admin_site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # เส้นทางหลักของเว็บไซต์
    path('', views.home_view, name='home'),
    path('index/', views.home_view, name='home'),
    path('ta_style/', views.ta_style, name='ta_style'),
    path('infocus/', views.infocus_view, name='infocus'), 
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'), 
    path('services/', views.services_view, name='services'),
    path("projects/<uuid:pk>/", views.projects_detail, name="projects_detail"),
    path('services/<slug:slug>/', views.services_detail, name='services_detail'),
    path('search/', views.global_search, name='global_search'),
    # จัดการเอกสาร
    path('documents/', views.document_list, name='document_list'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # จัดการ Favicon
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'core/images/favicon.ico')),
]

# การตั้งค่าสำหรับแสดงผลรูปภาพ (Media)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)