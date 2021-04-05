"""bookstore_project URL Configuration

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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # Replace built-in auth app with django-allauth
    # path('accounts/', include('django.contrib.auth.urls')),

    #Local apps
    path('', include('pages.urls')),
    path('books/', include('book.urls')),
    
    # Delete users.urls and instead use django-allauth
    # path('accounts/', include('users.urls')),  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
