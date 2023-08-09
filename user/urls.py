from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/',views.signup.as_view()),
    path('login/',views.login.as_view()),
    path('ckeck_tocken/',views.ckeck_tocken.as_view()),
    path('add_address/', views.add_address.as_view()),
    path('update_profile_photo/', views.update_profile_photo.as_view()),
    path('edit_address/', views.edit_address.as_view()),
    path('get_wallet_balance/', views.get_wallet_balance.as_view()),
    path('get_address/', views.get_address.as_view()),
    path('get_wallet_transaction/', views.get_wallet_transaction.as_view()),
    path('trasaction_history/', views.trasaction_history.as_view()),
    path('new_transaction/', views.new_transaction.as_view()),
]