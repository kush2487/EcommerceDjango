from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from products.models import Products,Category
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.serializers import ProductSerializer, CategorySerializer


# # Create your views here. 


# Product Views
def changing_api(request):
    data = Products.objects.all()
    d = data[0]
    d.name = 'testing_124'
    d.save()
    data = Products.objects.all()
    print(data)
    return HttpResponse(data)


@api_view(['GET'])
def get_products(request):
    # data = Products.objects.all()
    # serializerProducts = ProductSerializer(data, many = True)
    # return Response(serializerProducts.data)

    products = Products.objects.all()

    #searching products by name 

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains = search)
    
    #fetching the category 
    category_id = request.GET.get("category")

    if category_id: 
        products = products.filter(category_id = category_id)

    #geting the data if min and max price given
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    try:
        if min_price:
            products = products.filter(price__gte = min_price)
        if max_price:
            products = products.filter(price__lte = max_price)
    except ValueError:
        return Response({
                "message" : "something wrong in the code"
        },
        status=status.HTTP_400_BAD_REQUEST
        )
    #checking if the stock is available

    stock = request.GET.get('stock')
    if stock:
        products = products.filter(stock__gte = stock)
    

    #getting if the available or not 
    is_available = request.GET.get('is_availabel')
    if is_available is not None:
        if is_available.lower == 'true':
            products = products.filter(is_available = True)
        elif is_available.lower == 'false':
            products = products.filter(is_available = False)

    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)




@api_view(['GET'])
def get_products_id(request, id):
    try:
        data = Products.objects.get(id = id )
        serializerProducts = ProductSerializer(data)
        return Response(serializerProducts.data)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creating_product(request):
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(created_by = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    try:
        product = Products.objects.get(id = id)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product_full(request, id):
    try:
        product = Products.objects.get(id = id)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    try:
        product = Products.objects.get(id = id)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response({"message": "Product Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)



# Category Views 
@api_view(['GET'])
def get_all_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategorySerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, id ):
    try:
        category = Category.objects.get(id = id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    category.delete()
    return Response({"message":" Category Successfully Deleted Along with linked products"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_product(request):
    products = Products.objects.filter(created_by = request.user)

    serializer = ProductSerializer(products, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)
