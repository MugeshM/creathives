from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.load, name="index"),
    url(r'^jwt/', views.getjwt, name='jwt'),
    url(r'^login/',views.login,name="login"),
    url(r'^logintkn/',views.logintkn,name="login"),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^logout/',views.logout_view,name="logout"),
    url(r'^settings/',views.settings,name="settings"),
    url(r'^updateprofile/',views.updateprofile,name="updateprofile"),
    url(r'^updatecover/',views.updatecover,name="updatecover"),
    url(r'^updateimg/',views.updateimg,name="updateimg"),
    url(r'^token/', views.token, name='token'),
    url(r'^projupdate/', views.projectdetailupdate, name='projupdate'),
    url(r'^uploadprojthumb/', views.uploadprojthumb, name='uploadprojthumb'),
    url(r'^deleteproject/', views.deleteproject, name='deleteproject'),
    url(r'^handlemediaupload/', views.handlemediaupload, name='handlemediaupload'),
    url(r'^mediadetails/', views.mediadetails, name='mediadetails'),
    url(r'^updatemedia/', views.updatemedia, name='updatemedia'),
    url(r'^deletemedia/', views.deletemedia, name='deletemedia'),
]
