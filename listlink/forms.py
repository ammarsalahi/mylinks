
import hashlib
from django import *
from django import forms
from listlink.models import *
from django.contrib import messages

class_attrs='form-control form-control-lg'

class ListLinkForm(forms.ModelForm):
    class Meta:
        model=ListLink
        fields=('title','password')
        widgets={
            'title':forms.TextInput(attrs={'class':class_attrs}),
            'password':forms.PasswordInput(attrs={'class':class_attrs}),
        }
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(ListLinkForm,self).__init__(*args,**kwargs)
    def save_link(self):
        lilink=ListLink.obj.create_link(
            title=self.cleaned_data['title'],
            user=self.user,
            password=self.cleaned_data['password']
        )
        lilink.save()
        return lilink

class AddLinksForm(forms.Form):
    url=forms.URLField(label='')
    def save_link(self):
        ulink=UrlLink(
            url=self.cleaned_data['url']
        )
        ulink.save()
        return ulink


class PasswordLinkForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'id':'pass','class':class_attrs}))
    def __init__(self,id,request,*args,**kwargs):
        self.id=id
        self.request=request
        super(PasswordLinkForm,self).__init__(*args,**kwargs)
    def checkpw(self,pw,pw2):
        pw=hashlib.sha3_512(bytes(pw,encoding='utf-8')).hexdigest()
        if pw==pw2:
            return True
        else:
            return False        
    def clean(self):
        ps=self.cleaned_data['password']
        try:
            li=ListLink.objects.get(shorturl=self.id)
            if not self.checkpw(pw=ps,pw2=li.password):
                self.add_error('password','')
                messages.error(self.request,'گذرواژه وارد شده نادرست است',extra_tags='getpass')
            else:
                self.request.session['chps']=1    
        except ListLink.DoesNotExist:
            return None     


                