from django.urls import path,include
from biolink.api_views import *
from biolink.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('',editSocial)
app_name='bio'
urlpatterns=[
    path('add/',login_required(Create_BiolinkView.as_view()),name='add'),
    path('edit/',login_required(Update_BioLink.as_view()),name='edit'),
    path('delete/',login_required(deleteBio),name="delete"),
    path('',showBio,name='show'),
    path('addsocials/',addSocialBio,name='addsocialbio'),
    path('socialapi/',getaddSocials),
    path('delsocial/<int:id>',deleteSocial),
    path('socials/',login_required((include(router.urls))))
]