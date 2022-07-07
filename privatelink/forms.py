from django import forms
from link.models import *
from privatelink.models import PrivateLink
from utils.choices import choice_u
class_attrs='form-control form-control-lg'


class PrivateLinkAddForm(forms.Form):
    title=forms.CharField(label='عنوان',widget=forms.TextInput(attrs={'class':class_attrs}))
    url=forms.URLField(label='آدرس',widget=forms.URLInput(attrs={'class':class_attrs}))
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(PrivateLinkAddForm,self).__init__(*args,**kwargs)    
    def save(self,request):
        plink=PrivateLink(
            title=self.cleaned_data['title'],
            user=self.user,
            link=Link.obj.Create_Link(
                url=self.cleaned_data['url'],
                linktype=choice_u[1]
            )
        )
        plink.save()
        return plink    
class PrivateEditForm(forms.ModelForm):
    class Meta:
        model=PrivateLink
        fields=('title',)
        widgets={
            'title':forms.TextInput(attrs={'class':class_attrs})
        }        