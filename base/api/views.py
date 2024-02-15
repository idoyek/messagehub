from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from base.models import Message
from .serializers import MessageSerializer


@api_view(['POST'])
def WriteMessage(request):
    message = MessageSerializer(data=request.data)
    message.is_valid(raise_exception=True)
    try:
        message.save()
    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(message.data, status=HTTP_201_CREATED)

@api_view(['GET'])
def GetReceivedMessages(request, user_id):
    try:
        messages = Message.objects.filter(receiver=user_id)
    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=HTTP_200_OK)

@api_view(['GET'])
def GetReceivedUnreadMessages(request, user_id):
    try:
        messages = Message.objects.filter(receiver=user_id, is_read=False)
    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    serialized_messages = MessageSerializer(messages, many=True)
    return Response(serialized_messages.data, status=HTTP_200_OK)

@api_view(['PUT'])
def ReadMessage(request, user_id):
    try:
        message = Message.objects.filter(receiver_id=user_id, is_read=False).order_by('creation_date').first()
        if not message:
            return Response({"message": "No unread messages found for this user."}, status=HTTP_400_BAD_REQUEST)
        message.is_read = True
        message.save()

    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['DELETE'])
def DeleteMessage(request, user_id):
    try:
        message = Message.objects.filter(receiver_id=user_id).order_by('creation_date').first()
        if not message:
            return Response({"message": "No messages to delete found for this user."}, status=HTTP_400_BAD_REQUEST)
        message.delete()

    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=HTTP_200_OK)
