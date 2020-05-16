from django.forms import ModelForm
from core.models import CurrentAccount, LoanAccount

class CurrentAccountForm(ModelForm):
    class Meta:
        model = CurrentAccount
        fields = '__all__'
        exclude =('user',)

class LoanAccountForm(ModelForm):
    class Meta:
        model = LoanAccount
        fields = '__all__'
        exclude =('user','loanID')