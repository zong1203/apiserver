from rest_framework import serializers
from commodity.models import Commodity


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ("id","Account","Launched","Name","Deacription","Price","Amount","Position","Img1","Img2","Img3","Img4","Img5")

    def to_representation(self, value):
        data = super().to_representation(value)
        image = []
        for i in (data["Img1"],data["Img2"],data["Img3"],data["Img4"],data["Img5"]):
            if i:
                image.append(i)
        data["Image"] = image
        for i in range(1,6):
            data.pop(f"Img{i}")
        data["Description"] = data["Deacription"]
        data.pop("Deacription")
        return data