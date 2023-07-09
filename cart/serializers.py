from rest_framework import serializers
from cart.models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("Commodity_ID","Account","Seller")

    # def to_representation(self, value):
    #     data = super().to_representation(value)
    #     data["Description"] = data["Deacription"]
    #     data.pop("Deacription")
    #     image = []
    #     for i in (data["Img1"],data["Img2"],data["Img3"],data["Img4"],data["Img5"]):
    #         if i:
    #             image.append("image/get/?picture_name="+i)
    #     data["Image"] = image
    #     for i in range(1,6):
    #         data.pop(f"Img{i}")
    #     return data