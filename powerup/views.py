from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from core import helpers
from powerup.forms import CurrentAccountForm, LoanAccountForm
from core.models import CurrentAccount, LoanAccount, YouthBankUser
from core.helpers import create_loan_account , get_meta_score



# Create your views here.
@never_cache
def index(request):
    return render(request, 'index.html')


@never_cache
def infoView(request):
    return render(request, 'info.html')


@never_cache
def optionsView(request):
    return render(request, 'options.html')


@never_cache
def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            client_user = helpers.create_client()
            user = YouthBankUser.objects.create(
                user=user, clientID=client_user['clientID'], assigned_branchkey=client_user['assigned_branchkey'])
            user.save()
            return redirect('/main/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login/')
@never_cache
def mainView(request):
    return render(request, 'mainpage.html')


@login_required(login_url='/login/')
@never_cache
def currentAccountView(request):
    the_form = CurrentAccountForm()
    the_data = CurrentAccount.objects.filter(user=request.user).all()
    context = {'the_form' : the_form, 'the_data':the_data}
    return render(request, 'current.html',context)


@login_required(login_url='/login/')
@require_POST
@never_cache
def createCurrentAccount(request):
    youth_user_data = YouthBankUser.objects.filter(user=request.user).values('clientID')
    clientID= youth_user_data[0]['clientID']
    accountID = helpers.create_current_account(clientID)['accountID']
    currentAccount = CurrentAccount.objects.create(user=request.user,accountID=accountID)
    currentAccount.save()
    return redirect('/current/')

@login_required(login_url='/login/')
@never_cache
def loanAccountView(request):
    the_form = LoanAccountForm()
    the_data = LoanAccount.objects.filter(user=request.user).all()
    score = get_meta_score()
    context = {'the_data':the_data,'the_score':score,'the_form' : the_form}
    return render(request, 'loan.html',context)

@login_required(login_url='/login/')
@require_POST
@never_cache
def createLoanAccount(request):
    the_form = LoanAccountForm(request.POST)
    if the_form.is_valid():
        user_form = the_form.save(commit=False)
        user_form.user = request.user
        youth_user_data = YouthBankUser.objects.filter(user=request.user)
        clientID= youth_user_data.values('clientID')[0]['clientID']
        assigned_branchkey= youth_user_data.values('assigned_branchkey')[0]['assigned_branchkey']
        loanID = create_loan_account(clientID,assigned_branchkey)['loanID']
        user_form.loanID = loanID
        user_form.save()
    return redirect('/loan/')