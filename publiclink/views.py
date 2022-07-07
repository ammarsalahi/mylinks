from django.shortcuts import redirect, render
from django.views.generic.base import View
from link.forms import *
from link.models import Link
from publiclink.filters import PublicFilter
from publiclink.forms import *
from publiclink.models import *
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

class PublicLink_CreateView(View):
    def get(self,request,*args,**kwargs):
        context={
            'icons':'fas fa-globe',
            'title':'افزودن لینک عمومی',
            'bgs':'bg-success',
            'bgsb':'btn-success',
            'btntitle':'ایجاد',
            'form':PublicLinkAddForm(request.user)
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'link/addLink.html',context)
    def post(self,request,*args,**kwargs):
        form=PublicLinkAddForm(request.user,request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('list-publink')

def PublicLink_UpdateView(request,id):
    try:
        plink=PublicLink.objects.get(id=id)
        if request.method=='GET':
            form=PublicEditForm(instance=plink)
            form2=LinkFormedit(instance=plink.link)
            context={
                'icons':'fas fa-globe',
                'title':'ویرایش لینک عمومی',
                'bgs':'bg-success',
                'bgsb':'btn-success',
                'btntitle':'تایید',
                'form':form,
                'form2':form2
            }
            if request.user_agent.is_mobile:
                context['mobile']=1
            return render(request,'link/addLink.html',context)
        elif request.method=='POST':    
            form=PublicEditForm(request.POST,instance=plink)
            form2=LinkFormedit(request.POST,instance=plink.link)
            if form.is_valid() and form2.is_valid():
                form.save()
                form2.save()
                return redirect('list-publink')
    except PublicLink.DoesNotExist:
        return redirect('home')            

def PublicLinkList(request):
    plink=PublicFilter(request.GET,queryset=PublicLink.objects.filter(user=request.user).order_by('id'))
    p_page=Paginator(plink.qs,3)
    page_number=request.GET.get('page')
    page=p_page.get_page(page_number)
    context={
        'searchform':plink.form,
        'icons':'fas fa-globe',
        'page':page,
        'plist':page.object_list,
        'titleof':' لینک های عمومی',
        'urlss':'list-publink',
        'site':get_current_site(request),
        'publicss':1
    }
    if request.user_agent.is_mobile:
        context['mobile']=1
    return render(request,'link/list_link.html',context)

def PublicLinkDelete(request,id):
    plink=PublicLink.objects.get(id=id)
    plink.delete()
    return redirect('list-publink')

    