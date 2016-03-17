from django.shortcuts import render,render_to_response
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from calendar import timegm
from rest_framework import status
from models import User,projects
from django.contrib.auth import authenticate, login as auth_login
from .serializers import LoginSerializer,SignupSerializer,ProfileSerializer
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse

@login_required
def home(request):
     return render(request,"index.html")

def getjwt(request):
    return render(request,"jwttest.html")

@api_view(['POST'])
@permission_classes((AllowAny,))
def logintkn(request):
	print request.data
	email=request.data.get("email")
	user_pass=request.data.get("password")
	account = authenticate(email=email, password=user_pass)
        print account
        if account is not None:
            auth_login(request, account)
            serialized = LoginSerializer(account)
            return Response( { 'success_message': "You are an authorized user",
           			 },status=status.HTTP_200_OK)
        else:
            return Response( {
            'error_message':"Username/password is incorrect.",
            },status=status.HTTP_401_UNAUTHORIZED)


def login(request):
    return render(request,"login.html")

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    if request.method == 'POST':
        print request.POST
        print request.POST["email"]
        # data = JSONParser().parse(request)
        serializer = SignupSerializer(data=request.POST)

        if not serializer.is_valid():
            return Response({'error_message':"Registration Failed. Try Again",},status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.save()
            output_serializer = SignupSerializer(user)
     	    return Response( { 'success_message': "Account Created successfully. You can login now",
           			 },status=status.HTTP_201_CREATED)


def logout_view(request):
    logout(request)
    return render(request, "login.html")

@login_required
def settings(request):
    return render(request, "settings.html")

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def updateprofile(request):
    if request.method == 'POST':
        print request.data
        try:
            con = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        profile_serializer = ProfileSerializer(con, data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def updatecover(request):
    if request.method == 'POST':
        print request.data
        try:
            wallimgurl= request.POST.get("coverimgurl")
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        con =  User.objects.filter(id=request.user.id).update(wallimg_url=wallimgurl)
        return render(request,"index.html")

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def updateimg(request):
    if request.method == 'POST':
        print request.data
        try:
            profimgurl= request.POST.get("profileimgurl")
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        con =  User.objects.filter(id=request.user.id).update(profile_url=profimgurl)
        return render(request,"index.html")