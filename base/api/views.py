from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from base.models import Message
from .serializers import MessageSerializer
from .serializers import UserSerializer
from django.contrib.auth.models import User


@api_view(['POST'])
def WriteMessage(request):
    user_id = request.user.id
    request.data['sender'] = user_id

    message = MessageSerializer(data=request.data)
    message.is_valid(raise_exception=True)
    try:
        message.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(message.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def GetReceivedMessages(request):
    user_id = request.user.id
    try:
        messages = Message.objects.filter(receiver=user_id)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def GetReceivedUnreadMessages(request):
    user_id = request.user.id
    try:
        messages = Message.objects.filter(receiver=user_id, is_read=False)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def ReadMessage(request):
    user_id = request.user.id
    try:
        message = Message.objects.filter(receiver_id=user_id, is_read=False).order_by('creation_date').first()
        if not message:
            return Response({"message": "No unread messages found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        message.is_read = True
        message.save()

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def DeleteMessage(request):
    user_id = request.user.id
    try:
        message = Message.objects.filter(receiver_id=user_id).order_by('creation_date').first()
        if not message:
            return Response({"message": "No messages to delete found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        message.delete()

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if not username or not email or not password:
        return Response({"message": "Missing params."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')   
    if not username or not password:
        return Response({"message": "Missing params."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_loggedin_user(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
