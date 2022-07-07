from django.conf import settings
from django.shortcuts import redirect, render
from link.models import Link
from listlink.views import getListLink
from sharelink.views import getShareLink
from utils.utils import *
from link.forms import *
from django.contrib.auth.decorators import login_required
from privatelink.views import getPrivateLink
from django.contrib.sites.shortcuts import get_current_site
from biolink.views import *
def index(request):
    context={
        'site':get_current_site(request),
        'titleof':'لینکهای من'
    }
    if request.session.has_key('errorlink'):
        context['errorlink']=1
        del request.session['errorlink']
    if request.session.has_key('plnk'):
        try:
            plink=Link.objects.get(id=request.session['plnk'])
            context['plink']=plink
            context['linkt']=getIdType(plink)
            del request.session['plnk']
        except Link.DoesNotExist:
            context={}
    context['form']=LinkForm()
    context['uform']=HomeLinkForm(request.user)
    if request.user_agent.is_mobile:
        context['mobile']=1
        context['form']=LinkFormMobile()
        context['uform']=HomeLinkFormMobile(request.user)

    return render(request,'index.html',context)      



def directLink(request,linkid):
    if linkid[:2]=='s-':
        try:
            link=Link.objects.get(shorturl=linkid)
            if link.linktype=='public':
                return redirect(link.url)
            elif link.linktype=='upublic':
                return redirect(link.url)        
            elif link.linktype=='uprivate':
                return getPrivateLink(request,linkid)
            elif link.linktype=='ushare':
                return getShareLink(request,linkid)    
        except Link.DoesNotExist:
            return getListLink(request,linkid)
    else:
        return showbiopublic(request, linkid)


def createLink(request):
    if request.method=='POST':
        form=LinkForm(request.POST)
        if form.is_valid():
            form.save_link(request)
            return redirect('home')   
        else:
            request.session['errorlink']=1
            return redirect('home')

def create_homelink(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form =HomeLinkForm(request.user,request.POST)
            if form.is_valid():
                form.save(request)
                return redirect('home')    
            else:
                request.session['errorlink']=1
                return redirect('home')
    else:
        return redirect('login')            

def error_404(request,exception):
    return render(request, template_name='404.html')
    
