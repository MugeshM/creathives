from django.shortcuts import render,render_to_response
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from calendar import timegm
from rest_framework import status
from models import User,projects
from django.contrib.auth import authenticate, login as auth_login
from .serializers import LoginSerializer,SignupSerializer,ProfileSerializer,ProjectSerializer
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from .forms import UploadFileForm
from .helper import handle_uploaded_file
from .jwt_helper import get_token
from django.template import Context

@login_required
def home(request):
     project = projects.objects.filter(user_id=request.user.id)
     context = {'projects': project}
     return render(request,"index.html",context)

def getjwt(request):
    return render(request,"jwttest.html")

@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    print get_token(request.data.get("email"))
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
         if request.data.get("coverimgurl")!=None:
            print "Uploading only URL"
            try:
                wallimgurl= request.POST.get("coverimgurl")
            except User.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            con =  User.objects.filter(id=request.user.id).update(wallimg_url=wallimgurl)
            return render(request,"index.html")
         elif request.data.get("file")!=None:
              print "Uploading File"
              if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    handle_uploaded_file(request.FILES['file'],request.FILES['file'].name,request.user)
                    wallimgurl="/static/media/"+str(request.user)+"/"+str(request.FILES['file'].name)
                    con =  User.objects.filter(id=request.user.id).update(wallimg_url=wallimgurl)
                    return render(request,"index.html")
              else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def updateimg(request):
    if request.method == 'POST':
      if request.POST.get("profileimgurl")!=None:
        print request.data
        try:
            profimgurl= request.POST.get("profileimgurl")
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        con =  User.objects.filter(id=request.user.id).update(profile_url=profimgurl)
        return render(request,"index.html")
      elif request.data.get("file")!=None:
              print "Uploading File"
              if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    handle_uploaded_file(request.FILES['file'],request.FILES['file'].name,request.user)
                    profimgurl="/static/media/"+str(request.user)+"/"+str(request.FILES['file'].name)
                    con =  User.objects.filter(id=request.user.id).update(profile_url=profimgurl)
                    return render(request,"index.html")
              else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#
# @api_view(['POST'])
# @login_required()
# @permission_classes((AllowAny,))
# def updatecover(request):
#     print request.FILES['file'].name
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         handle_uploaded_file(request.FILES['file'],request.FILES['file'].name,request.user)
#         return HttpResponse('success')
#     else:
#         return HttpResponse('failure')

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def projectdetailupdate(request):
     if request.method == 'POST':
        # print request.data
        if request.data.get("flag")=="T":
          print "create"
          project_serializer = ProjectSerializer(data=request.data)

          if project_serializer.is_valid():
            project_serializer.save()
            data=project_serializer.data
            count= projects.objects.filter(user_id=request.data.get("user_id")).count()
            return Response({"data":data,"projcount":count})
          return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get("flag")=="detail":
            print "detail"
            print request.data
            # res=projects.objects.get(id=request.data.get("project_id"))
            # print res.project_desc
            serializer=ProjectSerializer(projects.objects.get(id=request.data.get("project_id")))
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif request.data.get("flag")=="update":
            print "update"
            print request.data.get("projid")
            try:
             con=projects.objects.get(id=request.data.get("projid"),user_id=request.data.get("user_id"));
            except User.DoesNotExist:
             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            count= projects.objects.filter(user_id=request.data.get("user_id")).count()
            serializer = ProjectSerializer(con, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data,"projcount":count})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def uploadprojthumb(request):
    if request.method == 'POST':
                    print request.FILES.get("image")
                    # form = UploadFileForm(request.POST, request.FILES)
                    handle_uploaded_file(request.FILES.get("image"),request.FILES.get("image").name,request.user)
                    profimgurl="/static/media/"+str(request.user)+"/"+str(request.FILES.get("image").name)
                    # con =  User.objects.filter(id=request.user.id).update(profile_url=profimgurl)
                    print profimgurl
                    return Response({'proj_url':profimgurl},status=status.HTTP_200_OK)
    else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def deleteproject(request):
    if request.method == 'POST':
        print request.data
        projects.objects.get(id=request.data.get("proj_id"),user_id=request.data.get("user_id")).delete()
        count= projects.objects.filter(user_id=request.data.get("user_id")).count()
        print count
        return Response({"projcount":count},status=status.HTTP_200_OK)