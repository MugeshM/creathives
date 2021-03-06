from django.shortcuts import render,render_to_response
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from calendar import timegm
from rest_framework import status
from models import User,projects, media
from django.contrib.auth import authenticate, login as auth_login
from .serializers import LoginSerializer,SignupSerializer,ProfileSerializer,ProjectSerializer, MediaSerializer
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from main.settings import development
import os
from .forms import UploadFileForm
from .helper import handle_uploaded_file,create_projectfolder, delete_projectfolder, mediaupload
from .jwt_helper import get_token
from django.template import Context
from django.http import QueryDict
import json
from django.core import serializers
from ast import literal_eval
import subprocess
from random import randint


@login_required
def home(request):
    return HttpResponseRedirect("home/")


def load(request):
     project = projects.objects.filter(user_id=request.user.id)
     context = {'projects': project}
     print request.path
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
    print "logout"
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
                wallimgurl= request.data.get("coverimgurl")
            except User.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            con =  User.objects.filter(id=request.user.id).update(wallimg_url=wallimgurl)
            return Response({"msg":"updated successfully","coverimgurl":wallimgurl},status=status.HTTP_200_OK)
         elif request.data.get("file")!=None:
              print "Uploading File"
              if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    handle_uploaded_file(request.FILES['file'],request.FILES['file'].name,request.user,"cover_img")
                    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(request.user)
                    filename, file_extension = os.path.splitext(dirpath+"/"+request.FILES['file'].name)
                    wallimgurl="/static/media/"+str(request.user)+"/"+str("cover_img"+file_extension)
                    con =  User.objects.filter(id=request.user.id).update(wallimg_url=wallimgurl)
                    return Response({"msg":"updated successfully","coverimgurl":wallimgurl},status=status.HTTP_200_OK)
              else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def updateimg(request):
    if request.method == 'POST':
      if request.data.get("profileimgurl")!=None:
        print request.data
        try:
            profimgurl= request.data.get("profileimgurl")
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        con =  User.objects.filter(id=request.user.id).update(profile_url=profimgurl)
        return Response({"msg":"updated successfully","profileimgurl":profimgurl},status=status.HTTP_200_OK)
      elif request.data.get("file")!=None:
              print "Uploading File"
              if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    handle_uploaded_file(request.FILES['file'],request.FILES['file'].name,request.user,"profile_img")
                    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(request.user)
                    filename, file_extension = os.path.splitext(dirpath+"/"+request.FILES['file'].name)
                    profimgurl="/static/media/"+str(request.user)+"/"+str("profile_img"+file_extension)
                    con =  User.objects.filter(id=request.user.id).update(profile_url=profimgurl)
                    return Response({"msg":"updated successfully","profileimgurl":profimgurl},status=status.HTTP_200_OK)
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
          data=request.data
          dict={"user_id":str(request.user.id)}
          dict.update(request.data.dict())
          project_serializer = ProjectSerializer(data=dict)

          if project_serializer.is_valid():
            project_serializer.save()
            data=project_serializer.data
            print "proj id :"+str(data.get("id"))
            create_projectfolder(request.user,"Project"+str(data.get("id")))
            count= projects.objects.filter(user_id=request.user.id).count()
            return Response({"data":data,"projcount":count,"flag":"create"})
          return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get("flag")=="detail":
            print "detail"
            print request.data
            # res=projects.objects.get(id=request.data.get("project_id"))
            # print res.project_desc
            serializer=ProjectSerializer(projects.objects.get(id=request.data.get("project_id")))
            mediadata=MediaSerializer(media.objects.filter(user_id=request.user.id,project_id=request.data.get("project_id"))[:2],many=True)
            mediacount=media.objects.filter(user_id=request.user.id,project_id=request.data.get("project_id"))[:2].count()
            return Response({"projdata":serializer.data,"mediacount":mediacount,'mediadata':mediadata.data},status=status.HTTP_200_OK)
        elif request.data.get("flag")=="update":
            print "update"
            print request.data.get("projid")
            try:
             con=projects.objects.get(id=request.data.get("projid"),user_id=request.user.id);
            except User.DoesNotExist:
             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            count= projects.objects.filter(user_id=request.user.id).count()
            dict={"user_id":str(request.user.id)}
            dict.update(request.data.dict())
            serializer = ProjectSerializer(con, data=dict)
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
                    handle_uploaded_file(request.FILES.get("image"),request.FILES.get("image").name,request.user,"")
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
        projects.objects.get(id=request.data.get("proj_id"),user_id=request.user.id).delete()
        if(media.objects.filter(project_id=request.data.get("proj_id"),user_id=request.user.id).count()):
            media.objects.filter(project_id=request.data.get("proj_id"),user_id=request.user.id).delete()
        delete_projectfolder(request.user,"Project"+str(request.data.get("proj_id")))
        count= projects.objects.filter(user_id=request.user.id).count()
        print count
        return Response({"projcount":count},status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def handlemediaupload(request):
   if(int(request.data.get("ytube"))==0):
           print "media"
           filename=request.FILES.get("file").name.replace(" ", "-")
           filename=filename.replace("(", "-")
           filename=filename.replace(")", "-")
           filename=filename.replace("#", "")
           fname, file_extension = os.path.splitext(filename)
           filename=fname+str(randint(0,2000))+file_extension
           mediaupload(request.FILES.get("file"),request.data.get("mediatype"),filename,request.user,"Project"+request.data.get('projid'))
           # 'user_id','project_id','media_type','media_url','media_thumbnail_url','media_details','media_title'
           media_url="/static/media/"+str(request.user)+"/"+"Project"+request.data.get('projid')+"/"+request.data.get("mediatype")+"/"+filename
           homeurl="/media/mugesh/Extra/STUDIES/Internship/Django/Creathives"+media_url
           fname, file_extension = os.path.splitext(media_url)
           # print filename+" "+file_extension
           outputurl="/media/mugesh/Extra/STUDIES/Internship/Django/Creathives"+fname+".jpg"
           print homeurl
           print outputurl
           thumburl=fname+".jpg"
           if(request.data.get("mediatype")!="article" and request.data.get("mediatype")!="image"):
                a=subprocess.call('ffmpeg -i {0} -ss 00:00:14.435 -filter  scale=w=260:h=213 -vframes 1 {1}'.format(homeurl,outputurl),shell=True)
                print "subprocess :"+str(a)
                if(request.data.get("mediatype")=="track"):
                    print a
                    thumburl="/static/images/media.jpg"
           elif(request.data.get("mediatype")=="article"):
                subprocess.call('convert -resize 260x213\! {0}[0] {1}'.format(homeurl,outputurl),shell=True)
           data={'user_id':request.user.id,'project_id':request.data.get('projid'),'media_url':media_url,'media_thumbnail_url':thumburl,'media_type':request.data.get("mediatype")}
           print data
           serializer=MediaSerializer(data=data)
           if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   else:
       print "ytube insert"
       dict={"user_id":str(request.user.id)}
       dict.update(request.data.dict())
       serializer=MediaSerializer(data=dict)
       if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def mediadetails(request):
   if(int(request.data.get("scroll"))==0):
      start,end=0,2
      if(int(request.data.get("mid"))==0):
        if(request.data.get("mtype")!=""):
            mediadata=MediaSerializer(media.objects.filter(user_id=request.user.id,media_type=request.data.get("mtype"),project_id=request.data.get("project_id"))[start:end],many=True)
            mediacount=media.objects.filter(user_id=request.user.id,media_type=request.data.get("mtype"),project_id=request.data.get("project_id"))[start:end].count()
        else:
            mediadata=MediaSerializer(media.objects.filter(user_id=request.user.id,project_id=request.data.get("project_id"))[start:end],many=True)
            mediacount=media.objects.filter(user_id=request.user.id,project_id=request.data.get("project_id"))[start:end].count()
        return Response({"mediacount":mediacount,'mediadata':mediadata.data},status=status.HTTP_200_OK)
      else:
          mediadata=MediaSerializer(media.objects.filter(user_id=request.user.id,id=request.data.get("mid"))[start:end],many=True)
          return Response(mediadata.data,status=status.HTTP_200_OK)
   else:
        print "scroll"
        start,end=int(request.data.get("start")),int(request.data.get("end"))
        if(request.data.get("mtype")!=""):
            mediadata=MediaSerializer(media.objects.filter(user_id=request.user.id,media_type=request.data.get("mtype"),project_id=request.data.get("project_id"))[start:end],many=True)
            mediacount=media.objects.filter(user_id=request.user.id,media_type=request.data.get("mtype"),project_id=request.data.get("project_id"))[start:end].count()
        else:
            mediadata=MediaSerializer(media.objects.filter(user_id=request.user.id,project_id=request.data.get("project_id"))[start:end],many=True)
            mediacount=media.objects.filter(user_id=request.user.id,project_id=request.data.get("project_id"))[start:end].count()
        return Response({"mediacount":mediacount,'mediadata':mediadata.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def updatemedia(request):
            try:
             con=media.objects.get(id=request.data.get("mid"),user_id=request.user.id,project_id=request.data.get("project_id"));
            except User.DoesNotExist:
             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            # count= media.objects.filter(user_id=request.user.id).count()
            dict={"user_id":str(request.user.id)}
            dict.update(request.data.dict())
            serializer = MediaSerializer(con, data=dict)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@login_required()
@permission_classes((AllowAny,))
def deletemedia(request):
    if request.method == 'POST':
        l=request.data.getlist("selectedmedia[]")
        print l
        d = [s.encode('ascii') for s in l]
        d=map(int, d)
        print d
        media.objects.filter(project_id=request.data.get("project_id"),id__in=d,user_id=request.user.id).delete()
        return Response({"msg":"Selected items Deleted successfully","deleted":d},status=status.HTTP_200_OK)

