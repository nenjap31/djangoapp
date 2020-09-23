from .serializers import AccountSerializer, UserSerializer, UserProfileSerializer
from .models import Account
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from djapp.permissions import CustomDjangoModelPermissions
from django.contrib.auth.models import User



class AccountList(APIView):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserProfileSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return User.objects.all()

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        accounts = self.get_object(pk)
        accounts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)