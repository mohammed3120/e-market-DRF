from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    product_reviews = serializers.SerializerMethodField(method_name="get_reviews", read_only = True)
    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self, product):
        reviews = product.product_reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

