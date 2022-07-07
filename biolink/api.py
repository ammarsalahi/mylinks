from rest_framework import serializers
from biolink.models import *

class SocialSerial(serializers.ModelSerializer):
    getimg=serializers.CharField(source='get_imgs',read_only=True)
    geturl=serializers.CharField(source='get_urls',read_only=True)
    class Meta:
        model=SocialMedia
        fields=('id','username','getimg','geturl','typesocial')

class BioSerial(serializers.ModelSerializer):
    social_media=SocialSerial(many=True,read_only=True)
    class Meta:
        model=BioLink
        fields=('social_media',)

class AddSocialSerial(serializers.Serializer):
    choice_type=[
        ('Telegram','تلگرام'),
        ('Signal','سیگنال'),
        ('Instagram','اینستاگرام'),
        ('Linkedin','لینکدین'),
        ('Whatsapp','واتساپ'),
        ('Youtube','یوتیوب'),
    ]
    typesocial=serializers.ChoiceField(choices=choice_type,write_only=True)
    username=serializers.CharField(write_only=True)
    id=serializers.CharField(write_only=True)
    def validate(self, attrs):
        return super().validate(attrs)
    def save(self):
        try:
            bio=BioLink.objects.get(id=self.validated_data['id'])
            bio.social_media.add(
                SocialMedia.objects.create(
                    username=self.validated_data['username'],
                    typesocial=self.validated_data['typesocial']
                )
            )
            bio.save()
            return bio
        except BioLink.DoesNotExist:
            return None    

