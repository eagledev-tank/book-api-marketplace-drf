from rest_framework import serializers
from order.models import Order, OrderItem
from user.serializers import ProfileSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitems', many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    profile_obj = ProfileSerializer(source='profile', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['profile']

    def get_total_price(self, obj):
        total_price = obj.get_total_price()
        return total_price

    def create(self, validated_data):
        user = self.context['request'].user
        profile = user.profile
        order = Order.objects.create(profile=profile, **validated_data)
        return order
