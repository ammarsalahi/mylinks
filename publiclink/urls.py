from unicodedata import name
from django.urls import path
from publiclink.views import *
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('add/',PublicLink_CreateView.as_view(),name='add-publink'),
    path('edit/<int:id>',PublicLink_UpdateView,name='edit-publink'),
    path('delete/<int:id>',PublicLinkDelete,name='del-publink'),
    path('',login_required(PublicLinkList),name='list-publink'),
]