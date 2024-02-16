from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.get_loggedin_user),
    path('register/', views.register),
    path('login/', views.user_login),
    path('messages/write/', views.WriteMessage),
    path('messages/receiver/', views.GetReceivedMessages),
    path('messages/receiver/unread/', views.GetReceivedUnreadMessages),
    path('messages/read/', views.ReadMessage),
    path('messages/delete/', views.DeleteMessage),
]