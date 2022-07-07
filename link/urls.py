from django.urls import path,include
from link.views import *
from biolink.views import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns=[
    path('',index,name='home'),
    path('<str:linkid>',directLink,name='linking'),
    path('linkc/',createLink,name='add-link'),
    path('ulink/',create_homelink,name='add-userlink'),
    path('public/',include('publiclink.urls')),
    path('private/',include('privatelink.urls')),
    path('share/',include('sharelink.urls')),
    path('list/',include('listlink.urls')),
    path("favicon.ico",RedirectView.as_view(url=staticfiles_storage.url("mylinkslogo.ico")),),

]