from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User_Info
from .serializers import User_InfoSerializer
from rest_framework import generics
import logging


class UserDetailView(generics.RetrieveAPIView):
    queryset = User_Info.objects.all()
    serializer_class = User_InfoSerializer
    lookup_field = 'id'

class UserCreateView(generics.CreateAPIView):
    queryset = User_Info.objects.all()
    serializer_class = User_InfoSerializer

class UserListView(generics.ListAPIView):
    queryset = User_Info.objects.all()
    serializer_class = User_InfoSerializer

class ItemsView(APIView):
    def get(self, request):
        items = User_Info.objects.all()
        serializer = User_InfoSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = User_InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class ItemDetailView(APIView):
    def get(self, request, pk):
        try:
            item = User_Info.objects.get(pk=pk)
            serializer = User_InfoSerializer(item)
            return Response(serializer.data)
        except User_Info.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            item = User_Info.objects.get(pk=pk)
        except User_Info.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = User_InfoSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        try:
            item = User_Info.objects.get(pk=pk)
            item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User_Info.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ItemByUUIDView(APIView):
    def get(self, request, uuid, format=None):
        try:
            item = User_Info.objects.get(uuid=uuid) 
            serializer = User_InfoSerializer(item) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User_Info.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        

logger = logging.getLogger(__name__)    
class ItemDeleteByUUID(APIView):
    def get(self, request, uuid, format=None):
        try:
            item = User_Info.objects.get(uuid=uuid)
            item.delete()
            logger.info(f"Item with UUID {uuid} deleted successfully via GET")
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        except User_Info.DoesNotExist:
            logger.error(f"Item with UUID {uuid} not found")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting item with UUID {uuid}: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, uuid, format=None):
        try:
            item = User_Info.objects.get(uuid=uuid)
            item.delete()
            logger.info(f"Item with UUID {uuid} deleted successfully via DELETE")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User_Info.DoesNotExist:
            logger.error(f"Item with UUID {uuid} not found")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting item with UUID {uuid}: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)