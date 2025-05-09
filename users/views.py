from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def registered_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username = username).exists():
        return Response(
            {
                "message" : "This user already exists"
            },
            status = status.HTTP_208_ALREADY_REPORTED
        )
    

    User.objects.create_user(username=username, password=password)
    return Response(
        {
            "message":"User Created successfully"
        },
        status = status.HTTP_201_CREATED
    )
