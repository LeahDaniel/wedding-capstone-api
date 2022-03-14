"""wedding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from weddingapi.views import (HostVendorView, HostView, MessageView,
                              RatingView, ReviewView, VendorView, login_user,
                              register_host, register_vendor)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'hosts', HostView, 'host')
router.register(r'vendors', VendorView, 'vendor')
router.register(r'messages', MessageView, 'message')
router.register(r'ratings', RatingView, 'rating')
router.register(r'reviews', ReviewView, 'review')
router.register(r'hostvendors', HostVendorView, 'host vendor')


urlpatterns = [
    path('registerhost', register_host),
    path('registervendor', register_vendor),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
