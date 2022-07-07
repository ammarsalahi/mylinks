from re import search
from rest_framework import status,response
from rest_framework.decorators import api_view
from biolink.api import AddSocialSerial, BioSerial,SocialSerial
from django.shortcuts import *
from rest_framework.viewsets import ModelViewSet

from biolink.models import BioLink, SocialMedia


@api_view(['GET','POST'])
def getaddSocials(request):
    if request.method=='GET':
        try:
            bio=BioLink.objects.get(user=request.user)
            serial=BioSerial(instance=bio)
            return response.Response(serial.data)
        except BioLink.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)    
    elif request.method=='POST':
        serial=AddSocialSerial(data=request.data)
        if serial.is_valid():
            serial.save()
            return response.Response(status=status.HTTP_200_OK)
        else:
            print(serial.error_messages)
            return response.Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def deleteSocial(request,id):
    if request.method=='DELETE':
        try:
            bio=BioLink.objects.get(user=request.user)
            bio.social_media.remove(SocialMedia.objects.get(id=id))
            bio.save()
            return response.Response(status=status.HTTP_200_OK)
        except BioLink.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)    

class editSocial(ModelViewSet):
    queryset=SocialMedia.objects.all()
    serializer_class=SocialSerial         
                
                


    



    
