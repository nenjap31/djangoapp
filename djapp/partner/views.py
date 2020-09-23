from .serializers import PartnerSerializer
from .models import Partner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class PartnerList(APIView):
    permission_classes = (IsAuthenticated,)
    """
    List all partners, or create a new partners.
    """
    def get(self, request, format=None):
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Partner.objects.get(pk=pk)
        except Partner.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        partners = self.get_object(pk)
        serializer = PartnerSerializer(partners)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
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
