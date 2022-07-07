from rest_framework.response import Response
from rest_framework.decorators import api_view
from listlink.api import *
from rest_framework import status


@api_view(['POST'])
def addLinkToList(request):
    if request.method=='POST':
        serial=AddLinkSerial(data=request.data)
        if serial.is_valid():
            listl=serial.save()
            return Response(status=status.HTTP_200_OK,data={'id':listl.id})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['GET'])
def getLinks(request,id):
    if request.method=='GET':
        try:
            listl=ListLink.objects.get(id=id)
            serial=LinkListSerial(instance=listl)
            return Response(serial.data)
        except ListLink.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)    

@api_view(['DELETE'])
def deleteLink(request,linkid,id):
    try:
        listl=ListLink.objects.get(id=linkid)
        listl.addlink.remove(UrlLink.objects.get(id=id))
        listl.save()
        return Response(status=status.HTTP_200_OK)
    except ListLink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)