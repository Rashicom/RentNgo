from rest_framework import serializers
from .models import CustomUser, Address,Wallet , Wallet_transaction

class Signup_serializer_user(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','contact_number','age', 'password']



class Login_serializer_user(serializers.Serializer):

    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


# for normal serializer for both address, state and countrie table
# after validation tables need to be explicitly updated
class Address_serializer(serializers.Serializer):

    country = serializers.CharField(required = True)
    state = serializers.CharField(required = True)
    address = serializers.CharField(required = True)
    place = serializers.CharField(required = True)
    city = serializers.CharField(required = True)
    zip_code = serializers.IntegerField(required = True)
    contact_number = serializers.CharField(max_length=12, required = False)


# update image serializer
class Update_image_serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields=['profile_photo']
    

class Edit_address_serializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        

class Wallet_transactions_serializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet_transaction
        fields = ['wallet_transaction_type','wallet_transaction_amount']


class Wallet_transactions_table_serializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet_transaction
        fields = '__all__'

