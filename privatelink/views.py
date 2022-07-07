from traceback import print_tb
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.views.generic.base import View
from link.forms import *
from link.models import Link
from privatelink.forms import *
from privatelink.models import *
from django.contrib.auth.decorators import login_required
from privatelink.filters import PrivateFilter
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
class PrivateLink_CreateView(View):
    def get(self,request,*args,**kwargs):
        context={
            'icons':'fas fa-eye-slash',
            'bgs':'bg-primary',
            'bgsb':'btn-primary',
            'btntitle':'ایجاد',
            'title':'افزودن لینک خصوصی',
            'form':PrivateLinkAddForm(request.user)
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'link/addLink.html',context)
    def post(self,request,*args,**kwargs):
        form=PrivateLinkAddForm(request.user,request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('list-prilink')

def PrivateLink_UpdateView(request,id):
    try:
        plink=PrivateLink.objects.get(id=id)
        if request.method=='GET':
            form=PrivateEditForm(instance=plink)
            form2=LinkFormedit(instance=plink.link)
            context={
                'icons':'fas fa-eye-slash',
                'title':'ویرایش لینک خصوصی',
                'bgs':'bg-primary',
                'bgsb':'btn-primary',
                'btntitle':'تایید',
                'form':form,
                'form2':form2
            }
            if request.user_agent.is_mobile:
                context['mobile']=1
            return render(request,'link/addLink.html',context)
        elif request.method=='POST':    
            form=PrivateEditForm(request.POST,instance=plink)
            form2=LinkFormedit(request.POST,instance=plink.link)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                return redirect('list-prilink')   
    except PrivateLink.DoesNotExist:
        return redirect('home')   
    
def PrivateLinkList(request):
    plink=PrivateFilter(request.GET,queryset=PrivateLink.objects.filter(user=request.user).order_by('id'))
    p_page=Paginator(plink.qs,3)
    page_number=request.GET.get('page')
    page=p_page.get_page(page_number)
    context={
        'searchform':plink.form,
        'icons':'fas fa-eye-slash',
        'page':page,
        'prlist':page.object_list,
        'titleof':'لینک های خصوصی',
        'icons':'fas fa-eye-slash',
        'urlss':'list-prilink',
        'site':get_current_site(request),
        'privatess':1

    }
    if request.user_agent.is_mobile:
        context['mobile']=1
    return render(request,'link/list_link.html',context)

def PrivateLinkDelete(request,id):
    plink=PrivateLink.objects.get(id=id)
    plink.delete()
    return redirect('list-prilink')

@login_required
def getPrivateLink(request,id):
    try:
        pl=PrivateLink.objects.get(link=Link.objects.get(shorturl=id))
        if request.user==pl.user:
            return redirect(pl.link.url)
        else:
            return redirect('home')    
    except PrivateLink.DoesNotExist:
        return redirect('home')    