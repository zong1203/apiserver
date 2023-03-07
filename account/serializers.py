from rest_framework import serializers
from account.models import Userfile


class UserfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userfile
        fields = '__all__'