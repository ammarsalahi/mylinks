from django import forms
from user.models import Activation, User
from crispy_forms.layout import *
from django.contrib import messages
from user.models import *
import re
from utils.class_style import class_attrs,style_attrs
from biolink.models import *
from privatelink.models import *
from publiclink.models import *
from sharelink.models import *
from listlink.models import *



regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
class LoginForm(forms.Form):
    username=forms.CharField(
        required=True,
        label="نام کاربری یا ایمیل",
        widget=forms.TextInput(attrs={'class':class_attrs,'style':style_attrs})
    )
    password=forms.CharField(
        required=True,label='گذرواژه',
        widget=forms.PasswordInput(attrs={'id':'pass','class':class_attrs,'style':style_attrs})
    )
    
    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(LoginForm,self).__init__(*args,**kwargs)
    
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        try:
            user=User.objects.get(username=username)
            if not user.check_password(password):
                self.add_error('password','')    
                messages.error(
                    request=self.request,
                    message='گذرواژه نادرست است',
                    extra_tags='login'
                )
        except User.DoesNotExist:
            self.add_error('username','')    
            messages.error(request=self.request,
            message='نام کاربری وجود ندارد',
            extra_tags='login'
        )
    

class RegisterForm1(forms.Form):
    email=forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class':class_attrs,'style':style_attrs})
    )
    fullname=forms.CharField(
        max_length=300,
        label='نام کامل',
        required=True,
        widget=forms.TextInput(attrs={'class':class_attrs,'style':style_attrs})
    )    
    password=forms.CharField(
        max_length=200,
        label='گذرواژه',
        widget=forms.PasswordInput(attrs={'id':'passs','class':class_attrs,'style':style_attrs})
    )
    repassword=forms.CharField(
        max_length=200,
        label='تکرار گذرواژه',
        widget=forms.PasswordInput(attrs={'id':'repasss','class':class_attrs,'style':style_attrs})
    )
    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(RegisterForm1,self).__init__(*args,**kwargs)


    def clean(self):
        email=self.cleaned_data['email']
        try:
                ue=User.objects.get(email=email)
                self.add_error('email','')
                messages.error(request=self.request,message='این رایانامه قبلا استفاده شده است',extra_tags='register')     
        except User.DoesNotExist:
                return None                               
    def sending(self,email):
        active=Activation.obj.create_register(
            email=email
        )
        active.sendEmail(subs='register')
        self.request.session['AI']=active.id

class ValidationForm(forms.Form):
    verifation_code=forms.CharField(
        required=False,
        max_length=9,
        label='کد اعتبارسنجی',
        widget=forms.TextInput(attrs={
            'class':class_attrs,
            'pattern':'[0-9]{4}-[0-9]{4}',
            'id':'valids',
            'style':style_attrs

        })
    )    
    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(ValidationForm,self).__init__(*args,**kwargs)
    def clean(self):
        try:
            active=Activation.objects.get(id=self.request.session['AI'])
            if self.cleaned_data['verifation_code']!=active.active_code:
                self.add_error('verifation_code','')
                messages.error(self.request,'کد وارد شده نادرست است',extra_tags='validcode')
        except Activation.DoesNotExist:
            self.add_error('verifation_code','')
            messages.error(self.request,'این کد منقضی شده است',extra_tags='validcode')


class RegisterFrom2(forms.Form):
    images=forms.ImageField(
        required=False,
        label='images',
        widget=forms.FileInput(attrs={'style':'display:none;','id':'pimgs'})
    )
    username=forms.CharField(
        max_length=300,
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class':class_attrs,'id':'theusern','style':style_attrs})
    ) 
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['profile_image','fullname','username','email']        
        widgets={
            'username':forms.TextInput(attrs={'class':class_attrs,'id':'usern'}),
            'fullname':forms.TextInput(attrs={'class':class_attrs,'id':'usern'}),
            'email':forms.EmailInput(attrs={'class':class_attrs,'id':'emailn'}),
            'profile_image':forms.FileInput(attrs={'style':'display:none;','id':'proimgs'})
        }

class passwordChangeForm(forms.Form):
    last_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class':class_attrs,'id':'lastpass','style':style_attrs}),
        label='گذرواژه فعلی'
    )
    new_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class':class_attrs,'id':'pass1','style':style_attrs}),
        label='گذرواژه جدید'
    )
    renew_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class':class_attrs,'id':'pass2','style':style_attrs}),
        label='تکرار گذرواژه جدید'
    )
    def __init__(self,user,request,*args,**kwargs):
        self.user=user
        self.request=request
        super(passwordChangeForm,self).__init__(*args,**kwargs)

    def clean(self):
        lastp=self.cleaned_data['last_password']
        if not self.user.check_password(lastp):
            messages.error(self.request,'گذرواژه فعلی نادرست است',extra_tags='passch')        
            self.add_error('last_password','')                
        return self.cleaned_data
    def save(self):
        new_p=self.cleaned_data['new_password']
        self.user.set_password(new_p)
        self.user.save()
        return self.user

       
class PasswordForgetForm(forms.Form):
    emailorusername=forms.CharField(
        label='نام کاربر یا ایمیل خود را وارد کنید',
        widget=forms.TextInput(attrs={'class':class_attrs,'style':style_attrs})
    )
    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(PasswordForgetForm,self).__init__(*args,**kwargs)
    def clean(self):
        emuser=self.cleaned_data['emailorusername']
        if re.fullmatch(regex,emuser):
            try:
                user=User.objects.get(email=emuser)
            except User.DoesNotExist:
                self.add_error('emailorusername','')
                messages.error(
                    request=self.request,
                    message='کاربری با این ایمیل ثبت نشده است',
                    extra_tags='forget'
                )    
        else:
            try:
                user=User.objects.get(username=emuser)
            except User.DoesNotExist:
                self.add_error('emailorusername','')
                messages.error(
                    request=self.request,
                    message='کاربری با این نام کاربری ثبت نشده است',
                    extra_tags='forget'
                ) 
    def save(self):
        active=Activation.obj.create_forget(
            user=User.objects.get(email=self.cleaned_data['emailorusername'])
        )    
        active.sendEmail(subs='بازگردانی رمز',request=self.request)    

class NewPasswordForm(forms.Form):
    password1=forms.CharField(
        label='گذرواژه جدید',
        widget=forms.PasswordInput(attrs={'class':class_attrs,'id':'passs'})
    )   
    password2=forms.CharField(
        label=' تکرار گذرواژه جدید',
        widget=forms.PasswordInput(attrs={'class':class_attrs,'id':'repasss'})
    ) 
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(NewPasswordForm,self).__init__(*args,**kwargs)
    def clean(self):
        passw=self.cleaned_data['password1']
        if self.user.password==passw:
            self.add_error('password1','')
            messages.error(
                    request=self.request,
                    message='گذرواژه ای انتخاب کنید که اکنون از آن استفاده نمی کنید',
                    extra_tags='newpass'
            )     
    def save(self):
        passw=self.cleaned_data['password1']
        self.user.set_password(passw)
        self.user.save()
        return self.user  
            
class CheckPasswordForm(forms.ModelForm):
    password=forms.CharField(
        label='گذرواژه خود را وارد کنید',
        widget=forms.PasswordInput(attrs={'class':class_attrs,'style':style_attrs}),
        required=True
    )
    def __init__(self,user,request,*args,**kwargs):
        self.user=user 
        super(CheckPasswordForm,self).__init__(*args,**kwargs)
    class Meta:
        model=DeleteReason
        fields=('reason','password')
        widgets={
            'reason':forms.Select(attrs={'class':'selectpicker p-1 '+class_attrs})
        }
    def clean(self):
        user=self.user
        if not user.check_password(self.cleaned_data.get('password')):
            self.add_error('password','')
            messages.error(
                request=self.request,
                message='کاربری با این نام کاربری ثبت نشده است',
                extra_tags='forget'
            )    
                        
        
            
    





        

        