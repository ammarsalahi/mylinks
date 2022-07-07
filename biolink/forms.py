from django import forms
from biolink.models import *
class_attrs='form-control form-control-lg'

class BioLinkForm(forms.ModelForm):
    class Meta:
        model=BioLink
        fields=('profile_image','comment','title')
        widgets={
            'comment':forms.Textarea(attrs={'rows':4,'class':class_attrs}),
            'title':forms.TextInput(attrs={'class':class_attrs}),
            'profile_image':forms.FileInput(attrs={'style':'display:none;','id':'proimgs'})
        } 
    def __init__(self,user,*args,**kwargs):
        self.user=user
        super(BioLinkForm,self).__init__(*args,**kwargs)       
    def save_bio(self):
        bio=BioLink(
            user=self.user,
            title=self.cleaned_data['title'],
            comment=self.cleaned_data['comment'],
            profile_image=self.cleaned_data['profile_image']
        )
        bio.save()
        return bio    
        
class SocialForm(forms.ModelForm):
    class Meta:
        model=SocialMedia
        fields=('username','typesocial')
        widgets={
            'username':forms.TextInput(attrs={'id':'usern','class':class_attrs}),
            'typesocial':forms.Select(attrs={'id':'types','class':'selectpicker p-1 '+class_attrs}),
        }
    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(SocialForm,self).__init__(*args,**kwargs)    
    def clean(self):
        username=self.cleaned_data.get('username')
        try:
            bio=Bio.objects.get(
                user=self.request.user,
                social_media=SocialMedia.objects.get(username=username)
            )
            self.add_error('username', '')
            return self.cleaned_data
        except Bio.DoesNotExist:
            return self.cleaned_data
            
    def svae_social(self,request):
        usern=self.cleaned_data['username']
        types=self.cleaned_data['typesocial']
        social=SocialMedia(
            username=usern,
            typesocial=types,
        )            
        social.save()
        bio=BioLink.objects.get(user=request.user)
        bio.social_media.add(social)
        bio.save()
        return bio
    