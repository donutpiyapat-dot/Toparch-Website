from core.admin import admin_site
from django.urls import path
from core import views 
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def redirect_admin_login(request):
    return redirect('/login/')

urlpatterns = [
    path('admin/login/', redirect_admin_login),  
    path('admin/', admin_site.urls),
    path('login/', views.custom_login, name='login'),
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
    path('documents/', views.document_list, name='document_list'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout')
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'core/images/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)