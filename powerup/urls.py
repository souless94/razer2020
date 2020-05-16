# helloworld/urls.py
from django.urls import path
from django.conf.urls.static import static
from powerup import views

urlpatterns = [
    path('',views.index),
    path('info/',views.infoView),
    path('options/',views.optionsView),
    path('login/',views.loginView),
    path('main/',views.mainView),
    path('current/',views.currentAccountView),
    path('create_current/',views.createCurrentAccount),
    path('loan/',views.loanAccountView),
    path('create_loan/',views.createLoanAccount),
    
]
