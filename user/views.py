from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from user.forms import *
from django.contrib.auth.decorators import login_required
from link.models import *
from user.models import Activation,User
from publiclink.models import *
from privatelink.models import *
from sharelink.models import *
from listlink.models import *
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.

class userLogin(View):
    def get(self,request,*args,**kwargs):
        context={
            'titleof':'ورود به حساب'
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        context['form']=LoginForm(request)
        context['colors']='#ced5ce'
        return render(request=request,template_name='user/login.html',context=context)
    def post(self,request,*args,**kwargs):
        context={
            'titleof':'ورود به حساب'
        }
        form =LoginForm(request,request.POST)
        if form.is_valid():
            user=User.objects.get(username=form.cleaned_data['username'])
            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            if request.user_agent.is_mobile:
                context['mobile']=1
            context['form']=form
            context['colors']='#ced5ce'
            context['error']=1
            return render(request,'user/login.html',context)

            

class UserRegister(SessionWizardView):
    template_name='user/register.html'
    form_list=[RegisterForm1,ValidationForm,RegisterFrom2]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profiles'))
    def post(self, *args, **kwargs):
        if self.steps.current=='0':
            form=self.get_form(data=self.request.POST,files=self.request.FILES)  
            email=self.request.POST['0-email']
            form.sending(email)
        return super().post(*args, **kwargs)    
    def get_form_kwargs(self, step=None):
        kwargs = super(UserRegister, self).get_form_kwargs(step)
        if step==u'0':
            kwargs['request']=self.request
        elif step==u'1':
            kwargs['request']=self.request
        return kwargs    
    def get_context_data(self, form,**kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.request.user_agent.is_mobile:
            context['mobile']=1
        context['titleof']='ثبت نام'    
        return context
    
    def done(self, form_list, **kwargs):
        create_user(form_list=form_list)
        return redirect('login')

def create_user(form_list):
    form_data=[form.cleaned_data for form in form_list]
    user=User.obj.create_publicuser(
        username=form_data[2]['username'],
        email=form_data[0]['email'],
        profile_image=form_data[2]['images'],
        fullname=form_data[0]['fullname'],
        password=form_data[0]['password']
    )
    return user    
        
    
def check_user(request):
    username=request.GET.get('user')
    data={}
    try:
        user=User.objects.get(username=username)
        data['messageu']=' نام کاربری در دسترس نیست'
    except User.DoesNotExist:
        data['messageu']=''
    return JsonResponse(data)  






def UserLogout(request):
    auth.logout(request)  
    return redirect('home')          

      
class ProfileEditView(View):
    def get(self,request,*args,**kwargs):
        user=request.user
        _user=User.objects.get(id=user.id)
        context={
            'form':ProfileForm(instance=_user),
            'profileedit':1,
            'btnv':'btn-outline-success',
            'btne':'btn-primary',
            'btnp':'btn-outline-warning',
            'btnd':'btn-outline-danger',
            'titleof':'ویرایش حساب'


        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'user/setting.html',context)
    def post(self,request,*args,**kwargs):
        user=request.user
        _user=User.objects.get(id=user.id)
        form=ProfileForm(request.POST,request.FILES,instance=_user)
        if form.is_valid():
            form.save()
            return redirect('user-set')
        return redirect('setting')    
        
class PasswordChangeView(View):
    def get(self,request,*args,**kwargs):
        form=passwordChangeForm(request.user,request)
        context={
            'form':form,
            'passwords':1,
            'btnv':'btn-outline-success',
            'btne':'btn-outline-primary',
            'btnp':'btn-warning',
            'btnd':'btn-outline-danger',
            'titleof':'تعییر گذرواژه'
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'user/setting.html',context)
    def post(self,request,*args,**kwargs):
        form=passwordChangeForm(request.user,request,request.POST)
        context={
            'form':form,
            'passwords':1,
            'titleof':'تعییر گذرواژه'
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return redirect('user-set')
        else:
            context['pserror']=1
            return render(request,'user/setting.html',context)    


def ProfileView(request):
    context={
        'plinks':PublicLink.objects.filter(user=request.user).count(),
        'prilinks':PrivateLink.objects.filter(user=request.user).count(),
        'slinks':ShareLink.objects.filter(username=request.user.username).count(),
        'lilinks':ListLink.objects.filter(user=request.user).count(),
        'profileview':1,
        'btnv':'btn-success',
        'btne':'btn-outline-primary',
        'btnp':'btn-outline-warning',
        'btnd':'btn-outline-danger',
        'titleof':'حساب کاربری' 
    }
    if request.user_agent.is_mobile:
        context['mobile']=1
    return render(request,'user/setting.html',context)                

class PasswordForgetView(View):
    def get(self,request,*args,**kwargs):
        context={
            'titleof':'فراموشی رمز'
        } 
        if request.user_agent.is_mobile:
            context['mobile']=1
        context['form']=PasswordForgetForm(request)  
        return render(request,'user/password_form.html',context)
    def post(self,request,*args,**kwargs):
        form=PasswordForgetForm(request,request.POST)
        if form.is_valid():
            form.save()
            return redirect('ps-success')
        else:
            context={} 
            if request.user_agent.is_mobile:
                context['mobile']=1
            context['form']=form
            context['error']=1
            return render(request,'user/password_form.html',context)    
            
def passwordResetSuccess(request):
    return render(request,'user/password_form.html',{'success':1})

class NewPasswordView(View):
    def get(self,request,uid,*args,**kwargs):
        context={}
        try:
            active=Activation.objects.get(active_code=uid)
            context['form']=NewPasswordForm(active.user)
            context['titleform']='فراموشی رمز'
            if request.user_agent.is_mobile:
                context['mobile']=1
            return render(request,'user/password_form.html',context)
        except Activation.DoesNotExist:
            return redirect('home')   
    def post(self,request,uid,*args,**kwargs):
        try:
            active=Activation.objects.get(active_code=uid)
            form=NewPasswordForm(active.user,request.POST)
            if form.is_valid():
                form.save()
                active.delete()
                return redirect('login')
            else:
                return render(request,'user/password_form.html',{'form':form,'errorn':1})
        except Activation.DoesNotExist:
            return redirect('home')        

class UserDeleteView(View):
    def get(self,request,*args,**kwargs):
        context={
            'formselect':CheckPasswordForm(request.user, request),
            'titleform':'حذف کاربر',
            'titleof':'حذف حساب'
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'user/password_form.html',context)
    def post(self,request,*args,**kwargs):
        form=CheckPasswordForm(request.user,request,request.POST)
        if form.is_valid():
            return redirect('user-acceptdel')
class UserDeleteCompleteView(View):
    def get(self,request,*args,**kwargs):
        context={
            'titleform':'حذف کاربر',
            'plinks':PublicLink.objects.filter(user=request.user).count(),
            'prilinks':PrivateLink.objects.filter(user=request.user).count(),
            'slinks':ShareLink.objects.filter(username=request.user.username).count(),
            'lilinks':ListLink.objects.filter(user=request.user).count(),
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'user/accept.html',context)    
    def post(self,request,*args,**kwargs):
        PrivateLink.obj.delete_all_link(request.user)
        PublicLink.obj.delete_all_link(request.user)
        ListLink.obj.delete_all_link(request.user)
        ShareLink.obj.delete_all_link(user=request.user.username)
        BioLink.obj.delete_bio(request.user)
        user=request.user
        user.delete()  
        return redirect('home')   
            
