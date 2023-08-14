from rest_framework import serializers
from account.models import Userfile


class UserfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userfile
        fields = ('Account',"Name","Email","Phonenumber","StudentID","Introduction","Favorite","Profliephoto")


class UserfileSerializer_for_profile(serializers.ModelSerializer):
    class Meta:
        model = Userfile
        fields = ('Account',"Name","Email","Phonenumber","Introduction","id")
    def to_representation(self, value):
        data = super().to_representation(value)
        data["account"] = data["Account"]
        data.pop("Account")
        data["nickname"] = data["Name"]
        data.pop("Name")
        data["mail"] = data["Email"]
        data.pop("Email")
        data["phone"] = data["Phonenumber"]
        data.pop("Phonenumber")
        data["intro"] = data["Introduction"]
        data.pop("Introduction")
        return data
