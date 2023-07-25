from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/',views.signup.as_view()),
    path('login/',views.login.as_view()),
    path('ckeck_tocken/',views.ckeck_tocken.as_view()),
    path('addaddress/', views.add_address.as_view()),
    
]