from rest_framework import serializers
from sharelink.models import ShareLink
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','profile_image','fullname']

class ShareUserSerial(serializers.ModelSerializer):
    persons=UserSerializer(many=True,read_only=True)
    class Meta:
        model=ShareLink
        fields=('persons',)

class ShareLinkSerial(serializers.Serializer):
    userid=serializers.CharField(write_only=True)
    id=serializers.CharField(write_only=True)
    def save(self):
        id=self.validated_data['id']     
        uid=self.validated_data['userid']     
        try:
            shlink=ShareLink.objects.get(id=id)
            shlink.persons.add(User.objects.get(username=uid))
            shlink.save()
            return shlink
        except ShareLink.DoesNotExist:
            return None    

