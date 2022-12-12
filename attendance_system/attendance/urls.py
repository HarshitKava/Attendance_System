from django.urls import path
from . import views
urlpatterns = [
    path('', views.Login, name='Login'),
    path('HomeFaculty/', views.HomeFaculty, name='HomeFaculty'),
    path('Edit/', views.EditTT, name='EditTT'),
    path('Build/', views.BuildTT, name='BuildTT'),
    path('GenerateQR/<str:courseid>/', views.GenerateQR, name='GenerateQR'),
    path('MarkAttendance/<str:courseid>/<str:date>/<str:time>/<str:key1>/<str:key2>/', views.MarkAttendance, name='MarkAttendance'),
    
    path('Logout/', views.LogoutUser, name='Logout'),
]