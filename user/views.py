from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import Signup_serializer_user, Login_serializer_user, Address_serializer, Update_image_serializer,Edit_address_serializer, Wallet_transactions_serializer, Wallet_transactions_table_serializer
from .models import Wallet, Wallet_transaction, Countries, States, Address
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import authenticate
from django.db import transaction
from datetime import date
from django.db.models import Q
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
        try:
            address_instence = Address.objects.select_related("state_id").get(user_id = user)
        except Exception as e:
                    print(e)
                    return Response({"details":"user not found"},status=404)
        
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


# new transaction
class new_transaction(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = Wallet_transactions_serializer

    def post(self, request, format=None):
        """
        fetching user and amound to be paid from the request and update
        """

        # fetching data and get wallet instence to update wattet transaction
        user = request.user
        wallet_instance = Wallet.objects.get(user_id = user)

        # serializing data
        serialized_data = self.serializer_class(data=request.data)
        
        # returning serializing error implicitly to the frond end.
        if serialized_data.is_valid(raise_exception=True):
            """
            fetch the data from the serailized data and update the data base
            then serializing the data and return back to user

            before updating the database we have to check the transaction type,
            and check the balance in the wallet to make a succussfull update,
            otherwise it returns a insufficiant balance warning
            """
            
            wallet_transaction_type = serialized_data.validated_data.get('wallet_transaction_type')
            wallet_transaction_amount = serialized_data.validated_data.get('wallet_transaction_amount')

            # buissiness logic for wallet balence cross match and upation
            # if the type is withdrowel
            if wallet_transaction_type == "WITHDRAWAL":
                """
                only withdrow the money from wallet if there are sufficient balance in the account
                otherwise it returns insufficiant balance
                """
                if wallet_transaction_amount > wallet_instance.account_balance:
                    return Response({"details":"insufficient balance"},status=403)
                else:
                    wallet_instance.account_balance = wallet_instance.account_balance - wallet_transaction_amount
            
            # if the type is deposit
            elif wallet_transaction_type == "DEPOSIT":
                wallet_instance.account_balance += wallet_transaction_amount
            
            # save the wallet instence
            wallet_instance.save()

            try:
                # creatiing wallet transaction and return response
                new_transaction = Wallet_transaction.objects.create(wallet_id = wallet_instance, wallet_transaction_type = wallet_transaction_type, wallet_transaction_amount = wallet_transaction_amount)

            except Exception as e:
                print(e)
                return Response({"details":"something went wrong"},status=403)

            # serializing the new transaction and return back to user
            # here a new serializer is used to return all data, class serializer only return type and amount
            transaction_serializer = Wallet_transactions_table_serializer(new_transaction)
            
            return Response(transaction_serializer.data,status=201)




# wallet balance
class get_wallet_balance(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        fetching user wallet balance
        """
        user = request.user
        wallet_instence = Wallet.objects.get(user_id = user)
        return Response({"balance":wallet_instence.account_balance},status=200)


# get vallet transaction by transactin id
class get_wallet_transaction(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Wallet_transactions_table_serializer

    def get(self, request, format=None):
        """
        thier function searching for a prticular transaction by transaction id
        which given by the user and fetching the transactin details and send back
        """

        # fetching data from params
        wallet_transaction_id = request.query_params.get('wallet_transaction_id')
        
        # fetching transaction details by given transaction id
        try:
            transaction = Wallet_transaction.objects.get(wallet_transaction_id = wallet_transaction_id)
        except Exception as e:
            print(e)
            return Response({"details":"transaction not found"},status=404)

        # serializing data if the tranacion found and return
        serialized_data = self.serializer_class(transaction)
        return Response(serialized_data.data,status=200)
        



# transaction history
class trasaction_history(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = Wallet_transactions_table_serializer

    def get(self, request, format=None):
        """
        filtering the users transaction history by date
        date_from is set to today date if date_from is not provided
        and to date set to None
        """

        # fetching data from params
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', date.today())

        # wallet instance to filter
        user = request.user
        wallet_instance = Wallet.objects.get(user_id=user)

        # filtering logic
        if date_from == None:
            transactions = Q(wallet_id=wallet_instance) & Q(wallet_transaction_date__lte=date_to)
        
        else:
            transactions = Q(wallet_id=wallet_instance) & Q(wallet_transaction_date__lte = date_to) & Q(wallet_transaction_date__gte = date_from)

        # filtering wallet transaction history and serializing data
        transactions = Wallet_transaction.objects.filter(transactions)
        serialized_data = self.serializer_class(transactions, many=True)
        
        return Response(serialized_data.data, status=200)




# ////////////////////// authentication api ////////////////////////

# checking tocken is valied or not
class ckeck_tocken(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        return Response({"details":"valied tocken"},status=200)
        

