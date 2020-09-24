from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, UserProfileSerializer, ProfileSerializer, SignupSerializer, ChangePasswordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from djapp.permissions import CustomDjangoModelPermissions
from django.contrib.auth.models import User
from djapp.pagination import PaginationHandlerMixin
from .models import Account


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class AccountList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = BasicPagination

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, format=None):
        if request.user.is_superuser:
            user = User.objects.all()
        else:
            current_user = request.user
            entry = Account.objects.get(user_id=current_user.id)
            partner = Account.objects.values_list('user_id').filter(partner_id=entry.partner_id)
            user = User.objects.filter(id__in=partner)
        page = self.paginate_queryset(user)
        if page is not None:
            serializer = self.get_paginated_response(UserProfileSerializer(page, many=True).data)
        else:
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
        if request.user.is_superuser:
            user = self.get_object(pk)
        else:
            partner = Account.objects.get(user_id=request.user.id)
            if partner.partner_id != pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                user = self.get_object(pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if request.user.is_superuser:
            user = self.get_object(pk)
        else:
            partner = Account.objects.get(user_id=request.user.id)
            if partner.partner_id != pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                user = self.get_object(pk)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):
    permission_classes = [IsAuthenticated,]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupUser(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePassword(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, format=None):
        self.object = self.get_object(request.user.id)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)