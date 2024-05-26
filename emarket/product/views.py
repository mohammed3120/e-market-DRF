from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Product, Review
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import ProductSerializer
from .filters import ProductFilter

from django.db.models import Avg

#pagination
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def get_all_products(request):
    products_list = Product.objects.all()
    filterset = ProductFilter(request.GET, queryset=products_list.order_by('id'))
    count = filterset.qs.count()

    resPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPage

    query_set = paginator.paginate_queryset(filterset.qs, request)

    serializer = ProductSerializer(query_set, many =True)
    return Response({"products":  serializer.data, 'per page': resPage, "count": count})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_product(request, pk):
    products_list = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(products_list, many =False)
    return Response({"product":  serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    data = request.data
    serializer = ProductSerializer(data = data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user = request.user)
        result = ProductSerializer(product, many=False)
        return Response({"product":  result.data})
    else:
        return Response(serializer.errors)
    


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id = pk)
    if product.user != request.user:
        return Response({"Error": "Sorry you can update this product"},
                        status=status.HTTP_403_FORBIDDEN)
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()
    serializer = ProductSerializer(product, many = False)
    return Response({"product": serializer.data}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id = pk)
    if product.user != request.user:
        return Response({"Error": "Sorry you can delete this product"},
                        status=status.HTTP_403_FORBIDDEN)
    
    product.delete()
    return Response({"product": "This product was deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, pk):
    product = get_object_or_404(Product, id = pk)
    user = request.user
    review = product.product_reviews.filter(user = user)
    data = request.data

    if data['rating'] <=0 or data['rating'] > 5:
        return Response({"error": "Please select between 1 and 5 only"},
                        status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {'rating': data["rating"], 'comment': data['comment']}
        review.update(**new_review)
        
        rating = product.product_reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({"details": "Product review updated"}, 
                        status=status.HTTP_200_OK)
    else:
        Review.objects.create(
            user = user, 
            product = product,
            rating = data['rating'],
            comment = data['comment']
        )
        rating = product.product_reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({"details": "Product review created"}, 
                        status=status.HTTP_200_OK)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    product = get_object_or_404(Product, id = pk)
    user = request.user
    review = product.product_reviews.filter(user = user)

    if review.exists():
        review.delete()
        rating = product.product_reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({"details": "Product review deleted"}, 
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": "Review not found"}, 
                        status=status.HTTP_404_NOT_FOUND) 