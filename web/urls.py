from django.conf.urls import url
from django.urls import path
from web.views import UserLogin
from .views import userdetails
from .views import delete_integration
from .views import index

urlpatterns = [
    path("",index,name="index"),
    path("user/", userdetails, name="home"),
    path("user/<int:id>/", delete_integration, name="home"),

]

