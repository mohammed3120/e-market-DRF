from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from product.models import Product
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data['order_items'] # order_items from templates not from relations in models
    if order_items and len(order_items) ==0:
        return Response({"error": "No order recieved"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum(item['price']*item['quantity'] for item in order_items)
        order = Order.objects.create(
            country = data['country'],
            state = data['state'],
            city = data['city'],
            street = data['street'],
            zip_code = data['zip_code'],
            phone_no = data['phone_no'],
            total_amount = total_amount,
            user =user
        )
        for item in order_items:
            product = Product.objects.get(id = item['product'])
            item_obj = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                quantity = item['quantity'],
                price = item['price']
            )
            product.stock -= item_obj.quantity
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({"orders": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response({"order details": serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_status_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    serializer = OrderSerializer(order, many=False)
    return Response({"order details": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response({"The order is deleted succesfully"}, status=status.HTTP_200_OK)