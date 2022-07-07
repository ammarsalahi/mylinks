
from rest_framework import generics,filters
from sharelink.api import *
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sharelink.models import *

class UserSearch(generics.ListAPIView):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    filter_backends=[filters.SearchFilter]
    search_fields=('fullname','username')

@api_view(['POST'])    
def ShareUsers(request):
    if request.method=='POST':
        serial=ShareLinkSerial(data=request.data)
        if serial.is_valid():
            data=serial.save()
            return Response(data={'id':data.id})

@api_view(["GET"])
def getShareUsers(request,id):
    if request.method=='GET':
        try:
            shlink=ShareLink.objects.get(id=id)
            serial=ShareUserSerial(instance=shlink)
            return Response(serial.data)
        except ShareLink.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
def delUserShare(request,id,username):
    if request.method=='DELETE':
        try:
            shlink=ShareLink.objects.get(id=id)
            shlink.persons.remove(User.objects.get(username=username))
            shlink.save()
            return Response(status=status.HTTP_200_OK)
        except ShareLink.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)   
        
