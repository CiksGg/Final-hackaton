
from rest_framework import serializers
from .models import *

from review.serializers import *

class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"



class ProductSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%d/%m/%Y  %H:%M:%S", read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'image','description','price','category','quantity', 'created_at', 'warning')
        # fields='__all__'
    
    def to_representation(self, instance):
        print(instance)
        representation = super().to_representation(instance)
        representation['seller']=instance.seller.email
        representation['category']=CategoryProductSerializer(instance.category).data

        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        # representation['rating'] = instance.average_rating
        representation['favorite'] = instance.favorits.count()
        representation["likes"] = instance.likes.count()
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['seller_id'] = user_id
        product= Product.objects.create(**validated_data)
        return  product
