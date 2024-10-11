from rest_framework import serializers
from order.models import Order, OrderItem
from user.serializers import ProfileSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def create(self, validated_data):
        # Kitobning mavjud sonini kamaytirish
        book = validated_data['book']
        quantity = validated_data['quantity']

        if book.stock < quantity:
            raise serializers.ValidationError(f"{book.title} dan {quantity} ta mavjud emas")

        book.stock -= quantity
        book.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Eski va yangi quantity ma'lumotlarini olish
        old_quantity = instance.quantity
        new_quantity = validated_data.get('quantity', instance.quantity)
        book = validated_data.get('book', instance.book)

        # Eski va yangi quantity'larni taqqoslash
        if new_quantity > old_quantity:
            # Agar yangi quantity katta bo'lsa, kitob zaxirasidan farqni olib tashlaymiz
            difference = new_quantity - old_quantity
            if book.stock < difference:
                raise serializers.ValidationError(f'{book.title} dan {new_quantity} ta mavjud emas')
            book.stock -= difference
        elif new_quantity < old_quantity:
            # Agar yangi quantity kichik bo'lsa, kitob zaxirasiga farqni qaytaramiz
            difference = old_quantity - new_quantity
            book.stock += difference

        book.save()

        return super().update(instance, validated_data)


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


class OrderStatusReportSerializer(serializers.ModelSerializer):
    total_books = serializers.SerializerMethodField()  # Annotatsiyada kiritilgan total_books maydoni
    total_price = serializers.SerializerMethodField()  # total_price maydoni

    class Meta:
        model = Order
        fields = ['status', 'total_books', 'total_price']  # Serializerda kerakli maydonlarni ko'rsatamiz

    def get_total_books(self, obj):
        return sum(item.quantity for item in obj.orderitems.all())

    def get_total_price(self, obj):
        return obj.get_total_price()
