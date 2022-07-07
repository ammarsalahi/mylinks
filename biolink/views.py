from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required

from biolink.forms import BioLinkForm, SocialForm
from biolink.models import BioLink, SocialMedia
from user.models import *
# Create your views here.
class Create_BiolinkView(View):
    def get(self,request,*args,**kwargs):
        try:
            bio=BioLink.objects.get(user=request.user)
            return redirect('bio:show')
        except BioLink.DoesNotExist:    
            context={
                'form':BioLinkForm(request.user),
                'titles':'افزودن بیو',
                'btntxt':'تایید'
            }
            if request.user_agent.is_mobile:
                context['mobile']=1
            return render(request,'bio/addBio.html',context)
    def post(self,request,*args,**kwargs):    
        form=BioLinkForm(request.user,request.POST,request.FILES)
        if form.is_valid():
            bio=form.save_bio()
            return redirect('bio:addsocialbio')
            
def addSocialBio(request):
    bio=BioLink.objects.get(user=request.user)
    if request.method=='GET':
        context={
            'bio':bio,
            'form':SocialForm(request)
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'bio/socialbio.html',context)
    
@login_required
def showBio(request):
    try:
        bio=BioLink.objects.get(user=request.user)
        context={
            'bio':bio,
            'form':SocialForm(request)
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'bio/showbio.html',context)
    except BioLink.DoesNotExist:
        return redirect('bio:add')    

class Update_BioLink(View):
    def get(self,request,*args,**kwargs):
        bio=BioLink.objects.get(user=request.user)
        context={
            'titles':'ویرایش',
            'form':BioLinkForm(request.user,instance=bio),
            'btntxt':'تایید'
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'bio/addBio.html',context)
    def post(self,request,*args,**kwargs):
        bio=BioLink.objects.get(user=request.user)
        form=BioLinkForm(request.user,request.POST,request.FILES,instance=bio)
        if form.is_valid():
            bio=form.save()
            return redirect('bio:show')

def deleteBio(request):
    bio=BioLink.objects.get(user=request.user)
    bio.delete()
    return redirect('bio:add')    
     
     
def showbiopublic(request,username):
    try:
        bio=BioLink.objects.get(user=User.objects.get(username=username))
        context={
            'bio':bio,
        }   
        if request.user_agent.is_mobile:
            context['mobile']=1  
        return render(request,'bio/bio.html',context)
    except BioLink.DoesNotExist:
        return redirect('home')

    
         