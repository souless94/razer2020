from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class YouthBankUser(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    clientID = models.CharField(max_length=255,blank=True)
    assigned_branchkey = models.CharField(max_length=255,blank=True)
    objects = models.Manager()

class CurrentAccount(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    accountID = models.CharField(max_length=255,blank=True)
    objects = models.Manager()

class LoanAccount(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    loanID = models.CharField(max_length=255,blank=True)
    amount  = models.FloatField(blank=True)
    loanName =models.CharField(max_length=255,blank=True)
    objects = models.Manager()