from rest_framework import serializers 
from django.shortcuts import get_object_or_404
from listlink.models import *

class LinkSerial(serializers.ModelSerializer):
    class Meta:
        model=UrlLink
        fields=('url','id')

class LinkListSerial(serializers.ModelSerializer):
    addlink=LinkSerial(many=True,read_only=True)
    class Meta:
        model=ListLink
        fields=('addlink',)

class AddLinkSerial(serializers.Serializer):
    url=serializers.CharField(write_only=True)
    id=serializers.CharField(write_only=True)
    def validate(self, attrs):
        try:
            listl=ListLink.objects.get(id=attrs['id'])
            if listl.addlink.all().count() >0:
                for link in listl.addlink.all():
                    if link.url==attrs['url']:
                        raise serializers.ValidationError('url is exist!!')
                    else:
                        return super().validate(attrs)    
            else:
                return super().validate(attrs) 
        except ListLink.DoesNotExist:
            return None

    def save(self):
        ulink=UrlLink(
            url=self.validated_data['url']
        )
        ulink.save()
        listl=get_object_or_404(ListLink,id=self.validated_data['id'])
        listl.addlink.add(ulink)
        listl.save()
        return listl    