from django.contrib import admin

# Register your models here.
from core import models
# Register your models here.
admin.site.register(models.YouthBankUser)
admin.site.register(models.CurrentAccount)
admin.site.register(models.LoanAccount)