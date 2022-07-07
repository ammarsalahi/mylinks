from getpass import getuser
from unicodedata import name
from django.urls import path
from sharelink.api_views import *
from sharelink.views import *
urlpatterns=[
    path('add/',Create_ShareLinkView.as_view(),name='add-share'),
    path('',ShareLinkList,name='list-shlink'),
    path('edit/<int:id>',Update_ShareLinkView,name='edit-shlink'),
    path('delete/<int:id>',DeleteShareLink,name="del-shlink"),
    path('users/<int:id>',AddUserToShare,name='addusershare'),
    path('getusers/',UserSearch.as_view()),
    path('adduser/',ShareUsers),
    path('showusers/<int:id>',getShareUsers),
    path('deluser/<int:id>/<str:username>',delUserShare),

]