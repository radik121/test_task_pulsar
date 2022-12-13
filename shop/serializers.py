from rest_framework import serializers
from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'sku', 'price', 'status', 'image']

    def get_image(self, product):
        request = self.context.get('request')
        image = product.image.url
        image = image.split('.')
        return {'path': image[0],
                'formats': list(product.image_formats())}
