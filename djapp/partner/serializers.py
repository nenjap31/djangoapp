from rest_framework import serializers
from .models import Partner


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partner
        fields = ('id','name', 'email','address', 'status')