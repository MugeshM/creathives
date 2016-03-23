import os
from main.settings import development
def handle_uploaded_file(f,fname,username):
    # print os.path.dirname(os.path.abspath(__file__))
    # print os.path.isdir(os.path.dirname(os.path.abspath(__file__)))
    # print username
    # print str(development.PROJECT_ROOT)+"/static/media/"+str(username)
    dirpath=str(development.PROJECT_ROOT)+"/static/media/"+str(username)
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
