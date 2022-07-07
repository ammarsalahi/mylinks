from django.http import request
from django.shortcuts import redirect, render
from django.template import context
from django.views.generic.base import View
from sharelink.api import UserSerializer
from sharelink.filters import ShareFilter
from sharelink.forms import AddUserForm, ShareLinkEditForm, ShareLinkForm
from sharelink.models import ShareLink
from user.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from link.models import Link
from link.forms import *
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

class Create_ShareLinkView(View):
    def get(self,request,*args,**kwargs):
        context={
            'form':ShareLinkForm(request.user),
            'icons':'fas fa-share-alt',
            'title':'افزودن لینک اشتراکی',
            'bgs':'bg-secondary',
            'bgsb':'btn-secondary',
            'btntitle':'ایجاد',
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'link/addLink.html',context)
    def post(self,request,*args,**kwargs):
        form=ShareLinkForm(request.user,request.POST)
        if form.is_valid():
            shlink=form.save_link()
            return redirect('addusershare',id=shlink.id)

def AddUserToShare(request,id):
    if request.method=='GET':
        context={}
        srch=str(request.GET.get('srch'))
        if srch:
            context['users']=User.objects.filter(username__icontains=srch)
        context['idss']=id  
        if request.user_agent.is_mobile:
            context['mobile']=1  
        return render(request,'link/addusertoshare.html',context)
    elif request.method=='POST':
        return redirect('list-shlink')

    
@login_required
def getShareLink(request,id):
    try:
        sl=ShareLink.objects.get(link=Link.objects.get(shorturl=id))
        for user in sl.persons.all():
            if user==request.user:
                return redirect(sl.link.url)
                
            else:
                return redirect('home')    
    except ShareLink.DoesNotExist:
        return redirect('home')           

def ShareLinkList(request):
    shlink=ShareFilter(request.GET,queryset=ShareLink.objects.filter(username=request.user.username).order_by('id'))
    sh_page=Paginator(shlink.qs,9)
    page_number=request.GET.get('page')
    page=sh_page.get_page(page_number)
    context={
        'searchform':shlink.form,
        'shlist':page.object_list,
        'titleof':' لینک های اشتراکی',
        'icons':'fas fa-share-alt',
        'page':page,
        'urlss':'list-shlink',
        'sharess':1
    }
    if request.user_agent.is_mobile:
        context['mobile']=1
    return render(request,'link/list_link.html',context)

def Update_ShareLinkView(request,id):
    try:
        plink=ShareLink.objects.get(id=id)
        if request.method=='GET':
            form=ShareLinkEditForm(instance=plink)
            form2=LinkFormedit(instance=plink.link)
            context={
                'icons':'fas fa-share-alt',
                'title':'ویرایش لینک اشتراکی',
                'bgs':'bg-secondary',
                'bgsb':'btn-secondary',
                'btntitle':'تایید',
                'form':form,
                'form2':form2
            }
            if request.user_agent.is_mobile:
                context['mobile']=1
            return render(request,'link/addLink.html',context)
        elif request.method=='POST':    
            form=ShareLinkEditForm(request.POST,instance=plink)
            form2=LinkFormedit(request.POST,instance=plink.link)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                return redirect('list-shlink')   
    except PrivateLink.DoesNotExist:
        return redirect('home')  

def DeleteShareLink(request,id):
    shlink=ShareLink.objects.get(id=id)
    shlink.delete()
    return redirect('list-shlink')    