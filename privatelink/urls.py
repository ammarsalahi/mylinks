from django.urls import path
from privatelink.views import *
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('add/',login_required(PrivateLink_CreateView.as_view()),name='add-prilink'),
    path('',login_required(PrivateLinkList),name='list-prilink'),
    path('edit/<int:id>',login_required(PrivateLink_UpdateView),name='edit-prilink'),
    path('delete/<int:id>',login_required(PrivateLinkDelete),name='del-prilink'),
]