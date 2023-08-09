from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# overriding usermanager
class CustomUserManager(BaseUserManager):

    # overriding user based authentication methord to email base authentiction
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given mail must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# custom customer for user 
# extrafields are added to by inheriting the django user
class CustomUser(AbstractUser):

    # field doesnot needed
    username = None
    last_name = None

    # extra fields
    email = models.EmailField(unique=True)
    user_otp = models.CharField(max_length=10, blank=True, null=True)
    contact_number = models.CharField(max_length=12)
    profile_photo = models.ImageField(upload_to="Profile_photos", null=True, blank=True)
    age = models.IntegerField()
    social_rank = models.FloatField(default=2.5)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

# country table
class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50, unique=True)


# state table
class States(models.Model):
    state_id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, unique=True)


# Custom user addess
# forign key referenced to the Custom user
class Address(models.Model):
    
    address_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    state_id = models.ForeignKey(States, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    place = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    contact_number = models.CharField(max_length=12, null=True, blank=True)


# wallet
class Wallet(models.Model):

    wallet_id = models.AutoField(primary_key=True)    
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account_balance = models.IntegerField(default=0)


# wallter transaction
class Wallet_transaction(models.Model):
    
    # choices
    class wallet_transaction_type_chices(models.TextChoices):
        DEPOSIT = "DEPOSIT",
        WITHDRAWAL = "WITHDRAWAL"
        

    wallet_transaction_id = models.AutoField(primary_key=True)
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    wallet_transaction_type = models.CharField(max_length=50, choices=wallet_transaction_type_chices.choices)
    wallet_transaction_date = models.DateField(auto_now_add=True)
    wallet_transaction_status = models.BooleanField(default=True)
    wallet_transaction_amount = models.IntegerField()
    