from django.urls import path
from listlink.views import *
from listlink.api_views import *
urlpatterns=[
    path('add/',ListLink_CreateView.as_view(),name='add-listlink'),
    path('edit/<int:id>',ListLink_UpdateView.as_view(),name='edit-listlink'),
    path('delete/<int:id>',DeleteListLink,name='delete-listlink'),
    path('addlinks/<int:id>',addLinks,name='add-links'),
    path('',ListLink_List,name='list-listlink'),
    path('check-pass/<str:linkid>',getPassword,name='get-pass'),
    path('addlinktolist/',addLinkToList),
    path('geturllink/<int:id>',getLinks),
    path('deletelink/<int:linkid>/<int:id>',deleteLink),
]