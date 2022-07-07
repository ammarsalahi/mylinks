from django.urls import path
from user.views import *
from django.contrib.auth.decorators import login_required

urlpatterns=[
    path('login/',userLogin.as_view(),name='login'),
    path('logout/',UserLogout,name='logout'),
    path('register/',UserRegister.as_view(),name='register'),
    path('edit/',login_required(ProfileEditView.as_view()),name='user-edit'),
    path('',login_required(ProfileView),name='user-set'),
    path('passwordchange/',login_required(PasswordChangeView.as_view()),name='ps-change'),
    path('passwordforget/',PasswordForgetView.as_view(),name='ps-forget'),
    path('passwordsuccess/',passwordResetSuccess,name='ps-success'),
    path('passwordchangenew/<str:uid>',NewPasswordView.as_view(),name='ps-change-new'),
    path('userch/',check_user),
    path('removeuser/',UserDeleteView.as_view(),name='user-del'),
    path('acceptremove/',UserDeleteCompleteView.as_view(),name='user-acceptdel'),


]