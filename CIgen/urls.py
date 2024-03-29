"""CIgen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import home_page, about_page, contact_page, login_page, register_page

from django.conf import settings
from django.conf.urls.static import static

# change ‘Django administration’ text
admin.site.site_header = "CIgen Admin"
admin.site.site_title = "CIgen Admin"
admin.site.index_title = "Welcome to CIgen Admin Portal"

urlpatterns = [
    path('', include('home.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),

    # path('', home_page),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/',login_page, name='login'),
    path('register/',register_page, name='register'),
]

# serve static files only on development environment
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    pass