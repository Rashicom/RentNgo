from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import Signup_serializer_user, Login_serializer_user, Address_serializer, Update_image_serializer,Edit_address_serializer
from .models import Wallet, Wallet_transaction, Countries, States, Address
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import authenticate
from django.db import transaction
# Create your views here.


# user signup
class signup(APIView):

    serializer_class = Signup_serializer_user
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        creating useer, recieving request.data and serialzing it, then
        if validated create new user return a newly generated jwt access and refresh tocken
        """
        print("request hit")
        # serializing request.data
        serialized_data = self.serializer_class(data=request.data)
        
        if serialized_data.is_valid(raise_exception=True):
            """
            if the data is validated password is hashed and creating new user.
            retunt with generated jwt tocken
            """

            # creating user and and set password, save() doesnt hash password
            hashed_password = make_password(serialized_data.validated_data['password'])
            user = serialized_data.save(password = hashed_password)
            
            # excluding password from the response and send response
            response_data = serialized_data.data

            # updating wallet table
            new_wallet = Wallet(user_id = user)
            new_wallet.save()

            # removing password from response and send response
            response_data.pop('password')
            print("user created")
            return Response(response_data,status=201)
            

# login
class login(APIView):

    serializer_class = Login_serializer_user
    permission_classes = [AllowAny]

    def post(self, reuqest, format=None):
        """
        validating the user credencials and generating access and regresh
        jwt tocken if the user is validated otherwise return error message
        """
        print("request hit")
        # serializing data
        seriazed_data = self.serializer_class(data=reuqest.data)

        # validating credencians, if credencials invalied error message
        # automatically send to frond end
        if seriazed_data.is_valid(raise_exception=True):
            
            # fetching credencials for validation
            email = seriazed_data.validated_data['email']
            password = seriazed_data.validated_data['password']

            # authenticate func returns user instence if authenticated
            user = authenticate(email = email, password = password)

            # if user is authenticated generate jwt
            if user is not None:
                
                print("login success")
                # generating jwt tocken
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                
                # returning response with access and refresh tocken
                # refresh tocken used to generate new tocken before tockens session expired
                return Response(          
                    {
                        "email":email,
                        "password":password,
                        "access":str(access),
                        "refresh":str(refresh)
                    },
                    status=201     
                )
            
            # if user none, wrong email or passord
            else:
                return Response({"details":"wrong email or password"}, status=401)


# update address table
class add_address(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = Address_serializer

    @transaction.atomic
    def post(self, request, format=None):
        
        # fetching data
        user = request.user
        serialized_data = self.serializer_class(data=request.data)

        # validating data, if exception found, message automaticaly send to the frond end
        if serialized_data.is_valid(raise_exception=True):
            """
            data is validated and we have 3 tables to update
            first country table, then usng the country instance state table is updated
            then only address table is updated
            """
            
            try:   
                # updation country table
                # created is true if record created, return false if record fetched
                new_country, country_created = Countries.objects.get_or_create(country = request.data['country'])

                # using country state instence is fetched if exist, created if state_created is true
                new_state, state_created = States.objects.get_or_create(country_id = new_country, state = request.data['state'])
                
                # update address table
                # new_state is needed to update address tabel,
                # becouse address table referencing state table
                new_address = Address(user_id=user, state_id=new_state, address=request.data['address'], place=request.data['place'], city=request.data['city'], zip_code=request.data['zip_code'], contact_number=request.data.get('contact_number'))
                new_address.save()

                # return response
                return Response(serialized_data.data, status=201)

            except Exception as e:
                print("exception found")
                print(e)
                return Response({"details":"somthing went wrong"},status=403)



# update profile picture
class update_profile_photo(APIView):
    
    permission_classes = [IsAuthenticated]
    serialzier_class = Update_image_serializer
    def patch(self, request, format=None):
        
        # fetching data(profile photo), and serializing it
        serialized_data = self.serialzier_class(request.user,data=request.data)
        
        # validating data
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            
            # returning response
            return Response({"details":"created"},status=201)
        
# edit address
class edit_address(APIView):

    permission_classes=[IsAuthenticated]
    serializer_class = Edit_address_serializer
    def patch(self, request, format=None):
        """
        updating user address details
        """
        address_instence = Address.objects.get(user_id = request.user)
        # serializing data
        serialized_data = self.serializer_class(address_instence,data = request.data, partial=True)
        
        # validating serialized data
        # if any exception found exception implicitly send back to frondend
        # raise_exception responsible for implicit return
        if serialized_data.is_valid(raise_exception=True):
            """
            serializer model class Address have one forign key.
            if the user wants to update the state or country we have to fetch the insance of the country or state
            and update in in the address side 
            """
            
            try:
                serialized_data.save()
                return Response(serialized_data.data, status=201)
            except Exception as e:
                print(e)
                return Response({"details": "something went wrong"},status=403)

# get address
class get_address(APIView):

    permission_classes = [IsAuthenticated]
    seriallizer_class = Address_serializer

    def get(self, request, format=None):
        """
        fetching user address details
        """

        # fetching user address details. using value() we can get dict
        # insted of query set.
        user = request.user
        address_instence = Address.objects.select_related("state_id").get(user_id = user)
       
        # serializing data
        serialized_data = self.seriallizer_class(
            data={
                "state": address_instence.state_id.state,
                "country": address_instence.state_id.country_id.country,
                "address": address_instence.address,
                "place": address_instence.place,
                "city": address_instence.city,
                "zip_code": address_instence.zip_code,
                "contact_number": address_instence.contact_number
            }
        )

        if serialized_data.is_valid():
            
            return Response(serialized_data.validated_data,status=200)
        else:
            return Response({"details":"something went wrong"},status=403)



# wallet balance
class wallet_balance(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        fetching user wallet balance
        """
        user = request.user
        wallet_instence = Wallet.objects.get(user_id = user)
        return Response({"balance":wallet_instence.account_balance},status=200)



class get_wallet_transactions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pass



# transaction history
class trasaction_history(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        pass


# ////////////////////// authentication api ////////////////////////

# checking tocken is valied or not
class ckeck_tocken(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        return Response({"details":"valied tocken"},status=200)
        

