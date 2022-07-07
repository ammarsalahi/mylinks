from urllib import request
from django.shortcuts import redirect, render
from django.views.generic.base import View
from link.models import Link
from listlink.forms import AddLinksForm, ListLinkForm,PasswordLinkForm
from listlink.models import ListLink, UrlLink
from listlink.filters import ListFilter
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site

class ListLink_CreateView(View):
    def get(self,request,*args,**kwargs):
        context={
            'form':ListLinkForm(request.user),
            'icons':'fas fa-list',
            'title':'افزودن لینک لیستی',
            'bgs':'bg-warning',
            'bgsb':'btn-warning',
            'btntitle':'ایجاد',
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'link/addLink.html',context)
    def post(self,request,*args,**kwargs):
        form=ListLinkForm(request.user,request.POST)
        if form.is_valid():
            listlink=form.save_link()
            return redirect('add-links',id=listlink.id)

class ListLink_UpdateView(View):
    def get(self,request,id,*args,**kwargs):
        listlink=ListLink.objects.get(id=id)
        context={
            'form':ListLinkForm(request.user,instance=listlink),
            'icons':'fas fa-list',
            'title':'ویرایش لینک لیستی',
            'bgs':'bg-warning',
            'bgsb':'btn-warning',
            'btntitle':'تایید',
        }
        if request.user_agent.is_mobile:
            context['mobile']=1
        return render(request,'link/addLink.html',context)
    def post(self,request,id,*args,**kwargs):
        form=ListLinkForm(request.user,request.POST,instance=ListLink.objects.get(id=id))
        if form.is_valid():
            listlink=form.save()
            return redirect('add-links',id=listlink.id)

def addLinks(request,id):
    scroll=''
    listlink=ListLink.objects.get(id=id)
    if listlink.addlink.all().count() > 4:
        scroll='overflow:scroll'
    if request.method=='GET':
        context={
            'listlink':listlink,
            'form':AddLinksForm(),
            'title':'افزودن لینک لیستی',
            'bgs':'bg-warning',
            'bgsb':'btn-warning',
            'btntitle':'ایجاد',
            'scroll':scroll,
            'idss':id
        }
        if request.user_agent.is_mobile:
            context['mobile']=1

        return render(request,'link/addlinkstolist.html',context)  

def ListLink_List(request):
    listl=ListFilter(request.GET,queryset=ListLink.objects.filter(user=request.user))
    l_page=Paginator(listl.qs,9)
    page_number=request.GET.get('page')
    page=l_page.get_page(page_number)
    context={
        'searchform':listl.form,
        'listl':page.object_list,
        'titleof':'لینک های لیستی',
        'icons':'fas fa-list',
        'page':page,
        'urlss':'list-listlink',
        'site':get_current_site(request),
        'listss':1
    }
    if request.user_agent.is_mobile:
        context['mobile']=1
    return render(request,'link/list_link.html',context)

def send_to_list(request):
    if request.method=='POST':
        return redirect('list-lilink')


def getListLink(request,id):
    if request.session.has_key('chps'):
        checked=True
    else:
        checked=False    
    try:
        li=ListLink.objects.get(shorturl=id)
        print(li.password)
        if li.password is not None and checked==False:
            return redirect('get-pass',linkid=id)
        else:
            return render(request,'link/showlistlink.html',{'links':li})   
    except ListLink.DoesNotExist:
        return redirect('home')    

def getPassword(request,linkid):
    if request.method=='GET':
        form=PasswordLinkForm(linkid,request)
        return render(request,'link/getpassword.html',{'form':form})
    elif request.method=='POST':
        form =PasswordLinkForm(linkid,request,request.POST)
        if form.is_valid():
            return redirect('linking',linkid=linkid)  
        else:
            return render(request,'link/getpassword.html',{'form':form,'error':1})

def DeleteListLink(request,id):
    listl=ListLink.objects.get(id=id)
    listl.delete()
    return redirect('list-listlink')


