from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('adminHome', views.adminHome, name='adminHome'),
    path('signUp', views.signUp, name='signUp'),
    path('logOut', views.logOut, name='logOut'),
    path('getStart', views.getStart, name='getStart'),
    path('updateUser', views.updateUser, name='updateUser'),
    path('updateBook', views.updateBook, name='updateBook'),
    path('borrowBook', views.borrowBook, name='borrowBook'),
    path('addBook', views.addBook, name='addBook'),
    path('myBook', views.backBook, name='myBook'),
    path('back', views.back, name='back'),
    path('extend', views.extend, name='extend'),
    path('browsingAdmin', views.browsingAdmin, name='browsingAdmin'),
    path('aboutUs', views.about, name='about'),

]
