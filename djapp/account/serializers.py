from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Account
from django.contrib.auth.models import User
from partner.models import Partner
from djapp.getuser import GetCurrentUser


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Partner
        fields = ('id', 'name', 'email', 'address', 'status')


class ProfileAccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = ('address', 'phone', 'birthdate')


class ProfileProSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    account = ProfileAccountSerializer(read_only=False)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email','account')

    def update(self, instance, validated_data):
        account = validated_data.pop('account')
        user_data = validated_data
        user_serializer = ProfileProSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(instance, user_data)
        account_serializer = ProfileAccountSerializer(instance.account,data=account)
        if account_serializer.is_valid():
            account_serializer.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','email','first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    partner = PartnerSerializer(read_only=False)

    class Meta:
        model = Account
        fields = ('address', 'phone', 'birthdate', 'partner')


class AccountsSerializer(serializers.HyperlinkedModelSerializer):
    partner_id = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ('address', 'phone', 'birthdate', 'partner_id')

    def update(self, instance, validated_data):
        request = GetCurrentUser.GetUser()
        instance.birthdate = validated_data.get('birthdate')
        instance.address = validated_data.get('address')
        instance.phone = validated_data.get('phone')
        if request.user.is_superuser:
            instance.partner_id = validated_data.get('partner_id')
        instance.save()
        return instance


class UsersProSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser',
            'date_joined')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    account = AccountsSerializer(required=False, many=False, read_only=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'is_superuser', 'date_joined', 'account')

    def update(self, instance, validated_data):
        account = validated_data.pop('account')
        user_data = validated_data
        user_serializer = UsersProSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(instance, user_data)
        account_serializer = AccountsSerializer(instance.account,data=account)
        if account_serializer.is_valid():
            account_serializer.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
