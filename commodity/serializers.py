from rest_framework import serializers
from commodity.models import Commodity

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ("id","Account","Launched","Name","Description","Price","Amount","BorrowedAmount","Position","Img1","Img2","Img3","Img4","Img5")

    def to_representation(self, value):
        data = super().to_representation(value)
        image = []
        for i in (data["Img1"],data["Img2"],data["Img3"],data["Img4"],data["Img5"]):
            if i:
                image.append("image/get/?picture_name="+i)
        data["imgs"] = image
        for i in range(1,6):
            data.pop(f"Img{i}")
        data["provider"] = data["Account"]
        data.pop("Account")
        data["name"] = data["Name"]
        data.pop("Name")
        data["description"] = data["Description"]
        data.pop("Description")
        data["price"] = data["Price"]
        data.pop("Price")
        data["amount"] = data["Amount"]
        data.pop("Amount")
        data["position"] = data["Position"]
        data.pop("Position")
        data["launched"] = data["Launched"]
        data.pop("Launched")
        return data