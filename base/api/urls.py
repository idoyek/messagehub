from django.urls import path
from . import views

urlpatterns = [
    path('messages/write/', views.WriteMessage),
    path('messages/receiver/<str:user_id>/', views.GetReceivedMessages),
    path('messages/receiver/unread/<str:user_id>/', views.GetReceivedUnreadMessages),
    path('messages/read/<str:user_id>/', views.ReadMessage),
    path('messages/delete/<str:user_id>/', views.DeleteMessage),
]