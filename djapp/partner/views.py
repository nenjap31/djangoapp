from rest_framework.pagination import PageNumberPagination
from .serializers import PartnerSerializer
from .models import Partner
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from djapp.permissions import CustomDjangoModelPermissions
from djapp.pagination import PaginationHandlerMixin
from account.models import Account
from djapp.getuser import GetCurrentUser


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class PartnerList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    pagination_class = BasicPagination

    def get_queryset(self):
        return Partner.objects.all()

    def get(self, request, format=None):
        if request.user.is_superuser:
            partners = Partner.objects.all()
        else:
            current_user = request.user
            part = Account.objects.get(user_id=current_user.id)
            partners = Partner.objects.filter(id=part.partner_id)
        page = self.paginate_queryset(partners)
        if page is not None:
            serializer = self.get_paginated_response(PartnerSerializer(page, many=True).data)
        else:
            serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerDetail(APIView):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return Partner.objects.all()

    def get_object(self, pk):
        try:
            return Partner.objects.get(pk=pk)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if request.user.is_superuser:
            partners = self.get_object(pk)
        partner = Account.objects.get(user_id=request.user.id)
        if partner.partner_id != pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            partners = self.get_object(pk)

        serializer = PartnerSerializer(partners)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if request.user.is_superuser:
            partners = self.get_object(pk)
        partner = Account.objects.get(user_id=request.user.id)
        if partner.partner_id != pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            partners = self.get_object(pk)
        serializer = PartnerSerializer(partners, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        partners = self.get_object(pk)
        partners.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
