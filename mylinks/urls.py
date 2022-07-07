
from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from link.views import *
from sharelink.views import *
from listlink.views import *
from biolink.views import *
from user.models import User
from django.contrib.auth.views import LoginView
from django.views.static import serve 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('user.urls')),
    path('bio/',include('biolink.urls')),
    path('',include('link.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/',include('allauth.urls')),
]   
urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404='link.views.error_404'