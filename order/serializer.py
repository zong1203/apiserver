from rest_framework import serializers
from order.models import Order
from account.models import get_primary_info_by_name
from commodity.models import get_name_and_img_by_id

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("Provider","Consumer","Progress","Order","Totalprice","Comment","Options","Using_Message","Selected_Option","Actual")

    def to_representation(self, value):
        data = super().to_representation(value)
        data["Provider"] = get_primary_info_by_name(data["Provider"])
        data["Consumer"] = get_primary_info_by_name(data["Consumer"])
        list = []
        for i in data["Order"]:
            name,img1 = get_name_and_img_by_id(i)
            temp = {
                "id": i,
                "name": name,
                "cover": "image/get/?picture_name=" + img1,
                "price": data["Order"][i]["price"],
                "amount": data["Order"][i]["amount"]
            }
            list.append(temp)
        data["Order"] = list
        return data