from decimal import Decimal
from store.models import Cart, CartItem, Product, Collection, Review
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True) # Calling the product serializer
    total_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity
    
class CartSerializer(serializers.ModelSerializer): 
    id = serializers.UUIDField()
    items = CartItemSerializer(many=True, read_only=True) # visit all id with its item
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'total_price']
    def get_total_price(self, cart: Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def save(self, *args, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']