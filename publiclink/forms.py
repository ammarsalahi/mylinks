from django import forms
from link.models import *
from publiclink.models import PublicLink
class_attrs='form-control form-control-lg'

choice_u=[
    ('upublic','عمومی'),
    ('uprivate','خصوصی'),
    ('ushare','اشتراکی'),
]

class PublicLinkAddForm(forms.Form):
    title=forms.CharField(label='عنوان',widget=forms.TextInput(attrs={'class':class_attrs}))
    url=forms.URLField(label='آدرس',widget=forms.URLInput(attrs={'class':class_attrs}))
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(PublicLinkAddForm,self).__init__(*args,**kwargs)    
    def save(self,request):
        plink=PublicLink(
            title=self.cleaned_data['title'],
            user=self.user,
            link=Link.obj.Create_Link(
                url=self.cleaned_data['url'],
                linktype=choice_u[0]
            )
        )
        plink.save()
        return plink

class PublicEditForm(forms.ModelForm):
    class Meta:
        model=PublicLink
        fields=('title',)
        widgets={
            'title':forms.TextInput(attrs={'class':class_attrs})
        }
