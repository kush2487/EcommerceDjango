from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import CartItem
from .serializers import CartItemSerializer
from products.models import Products


# Create your views here.

# To get all the items in the cart
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_item(request):
    try:
        items = CartItem.objects.get(user = request.user)
        serializer = CartItemSerializer (items, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_409_CONFLICT)



# to create a item in the cart 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get("product")
    quantity = request.data.get("quantity", 1)

    product = get_object_or_404(Products, id = product_id)

    created = CartItem.objects.get_or_create(user = request.user, product = product)
    item  = CartItem.objects.get_or_create(user = request.user, product = product)

    if not created :
        item += int(quantity)
    else:
        item = int(quantity)
    
    item.save()
    try:
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status = status.HTTP_204_NO_CONTENT)


# to change the items of a cart
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk = pk , users = request.user)
    quantity = request.data.get("quantity")

    if quantity:
        item.quantity = quantity
        item.save()
    
    serializer = CartItemSerializer(item)
    return Response (serializer.data, status = status.HTTP_201_CREATED)

# To delete a item from the cart
@api_view(['DELETED'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk = pk , user = request.user)
    item.delete()
    return Response("Item deleted", status=status.HTTP_204_NO_CONTENT)