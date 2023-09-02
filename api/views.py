from django.shortcuts import render, redirect
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from firstapp.models import Product
from rest_framework import status


@api_view(['GET'])
def get_products(request):

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_product(request):

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {'msg': 'Product added'}
        return Response(data=data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_product(request, pk):

    try:
        product = Product.objects.get(id=pk)
        product.delete()
        data = {'msg': 'App deleted'}
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        raise Http404