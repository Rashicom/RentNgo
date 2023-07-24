from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import Signup_serializer_user, Login_serializer_user, Address_serializer, Update_image_serializer
from .models import Wallet, Wallet_transaction, Countries, States, Address
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
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
                access = refresh.access_tocken
                
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
                new_address = Address(user_id=user, state_id=new_state, address=request.data['address'], place=request.data['place'], city=request.date['city'], zip_code=request.data['zip_code'], contact_number=request.data.get('contact_number'))
                
                # return response
                return Response(new_address, status=201)

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
        serialized_data = self.serialzier_class(data=request.data)
        
        # validating data
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            
            # returning response
            return Response({"details":"created"},status=201)
        

