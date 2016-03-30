import os
from main.settings import development
import shutil

def handle_uploaded_file(f,fname,username,ffname):
    # print os.path.dirname(os.path.abspath(__file__))
    # print os.path.isdir(os.path.dirname(os.path.abspath(__file__)))
    # print username
    # print str(development.PROJECT_ROOT)+"/static/media/"+str(username)
    print ffname
    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(username)
    filename, file_extension = os.path.splitext(dirpath+"/"+fname)
    # print file_extension
    print "fname"+fname
    if ffname!="":
        fname=ffname+file_extension
    print filename+"\n "+fname
    if os.path.isdir(dirpath):
       print "Dir Exists"
    else:
       os.mkdir(dirpath)
    # if os.path.isdir(dirpath):
    #    print "Dir Exists"
    # else:
    #    os.mkdir(dirpath)
    print development.PROJECT_ROOT
    with open(dirpath+"/"+fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def create_projectfolder(user,folname):
    print "sdfgdfasadsa"
    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(user)+"/"+folname
    print dirpath
    if os.path.isdir(dirpath):
       print "Dir Exists"
    else:
       print "Dirt"
       os.mkdir(dirpath)

def delete_projectfolder(user,folname):
    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(user)+"/"+folname
    if os.path.isdir(dirpath):
       print "Dir Exists"
       # os.rmdir(dirpath)
       shutil.rmtree(dirpath)
    else:
       print "Dirt"

def mediaupload(f,mtype,fname,username,folname):
    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(username)+"/"+folname+"/"+mtype
    if os.path.isdir(dirpath):
       print "Dir Exists"
    else:
       os.mkdir(dirpath)
    with open(dirpath+"/"+fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)