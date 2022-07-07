from django import forms
from link.models import *
from privatelink.models import PrivateLink
from user.models import User
from utils.utils import link_generator
from link.models import Link
from privatelink.models import PrivateLink
from publiclink.models import PublicLink
from sharelink.models import ShareLink
class_attrs='form-control form-control-lg'

        
class LinkForm(forms.ModelForm):
    url=forms.URLField(label='',widget=forms.TextInput(attrs={
        'class':class_attrs+' text-right',
        'dir':'ltr',
        'placeholder':'لینک مورد نظر را درج کنید...',
        'aria-describedby':'cutbtn',
        'style':"border-radius: 0px 50px 50px 0px"
    }))
    class Meta:
        model=Link
        fields=('url',)
    def save_link(self,request):
        link=Link.obj.Create_Link(
            url=self.cleaned_data['url'],
            linktype='public'
        )
        request.session['plnk']=link.id
        return link

class LinkFormMobile(forms.ModelForm):
    url=forms.URLField(label='',widget=forms.TextInput(attrs={
        'class':class_attrs+' text-right',
        'dir':'ltr',
        'placeholder':'لینک مورد نظر را درج کنید...',
        'aria-describedby':'cutbtn',
        'style':"border-radius: 50px 50px 50px 50px;height:50px;"
    }))
    class Meta:
        model=Link
        fields=('url',)
    def save_link(self,request):
        link=Link.obj.Create_Link(
            url=self.cleaned_data['url'],
            linktype='public'
        )
        request.session['plnk']=link.id
        return link
        
class LinkFormedit(forms.ModelForm):
    class Meta:
        model=Link
        fields=('url',)
        widgets={
            'url':forms.TextInput(attrs={'class':class_attrs+" text-left",'dir':'ltr'})
        }


def save(request,url,opt,user):
    link=Link.obj.Create_Link(
            url=url,
            linktype=opt
        )
    request.session['plnk']=link.id    
    if opt=='upublic':
        plink=PublicLink(
            user=user,
            link=link
        ).save()
        return plink
    elif opt=='uprivate':
        plink=PrivateLink(
            user=user,
            link=link
        ).save()
        return plink
    elif opt=='ushare':
        shlink=ShareLink(
            username=user.username,
            link=link
        ).save()
        return shlink    

class HomeLinkForm(forms.Form):
    url=forms.URLField(
        label='',
        widget=forms.TextInput(attrs={
            'class':class_attrs+' text-right',
            'style':"border-radius: 0px 50px 50px 0px",
            'dir':'ltr',
            'placeholder':'لینک مورد نظر را درج کنید...',
            'aria-describedby':'cutbtn',
        }),
    )
    opt=forms.CharField(label='',widget=forms.TextInput(attrs={'type':'hidden','id':'optss','value':'upublic'}))
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(HomeLinkForm,self).__init__(*args,**kwargs)
    def save(self,request):
        url=self.cleaned_data['url']
        opt=self.cleaned_data['opt']
        return save(request, url, opt, self.user)
        
class HomeLinkFormMobile(forms.Form):
    url=forms.URLField(
        label='',
        widget=forms.TextInput(attrs={
            'class':class_attrs+' text-right',
            'style':"border-radius: 50px 50px 50px 50px;height:50px",
            'dir':'ltr',
            'placeholder':'لینک مورد نظر را درج کنید...',
            'aria-describedby':'cutbtn',
        }),
    )
    opt=forms.CharField(label='',widget=forms.TextInput(attrs={'type':'hidden','id':'optss','value':'upublic'}))
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(HomeLinkFormMobile,self).__init__(*args,**kwargs)
    def save(self,request):
        url=self.cleaned_data['url']
        opt=self.cleaned_data['opt']
        return save(request, url, opt, self.user)               