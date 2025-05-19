from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),

    path('get_token/', views.getToken),

     path('create_member/',views.createMember),
     path('get_member/',views.getMember),
    path('record_leave/', views.recordLeaveTime, name='record_leave'),

     #path('delete_member/',views.deleteMember),
]
