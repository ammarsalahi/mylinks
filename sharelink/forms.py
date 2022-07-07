from email.policy import default
from django import forms
from link.models import Link
from sharelink.models import ShareLink
class_attrs='form-control form-control-lg'

class ShareLinkForm(forms.Form):
    title=forms.CharField(label='عنوان',widget=forms.TextInput(attrs={'class':class_attrs}))
    url=forms.URLField(label='آدرس',widget=forms.URLInput(attrs={'class':class_attrs}))
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(ShareLinkForm,self).__init__(*args,**kwargs)
 
    def save_link(self):
        shlink=ShareLink(
            username=self.user.username,
            title=self.cleaned_data['title'],
            link=Link.obj.Create_Link(
                url=self.cleaned_data['url'],
                linktype='ushare'
            )
        )
        shlink.save()
        return shlink

class AddUserForm(forms.Form):
    userid=forms.CharField(label='نام کاربری')

class ShareLinkEditForm(forms.ModelForm):
    class Meta:
        model=ShareLink
        fields=('title',)
        widgets={
            'title':forms.TextInput(attrs={'class':class_attrs})
        }

    