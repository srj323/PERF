from django.shortcuts import render
from django.http import HttpResponseRedirect
from Cibil.models import Credit_Card, Personal_Information, Application_History, Loan_Details, Loan_History
import random
from .forms import Information, Loan, Repayment
import datetime
from django.utils import timezone
from django.contrib.auth.models import User




# Create your views here.
def Loan_no(request):
    if request.method == 'POST':
        form = Loan(request.POST)
        if form.is_valid():
            loan = Loan_Details()
            no = form.cleaned_data['Creditcard']
            loan.Credit_Card_No = Credit_Card.objects.get(Credit_Card_No=no)
            credit = Credit_Card.objects.get(Credit_Card_No=no)
            print(credit.Username)
            loan.Loan_Type = 'Personal'
            loan.Loan_Amount = form.cleaned_data['Amount']
            loan.Loan_Duration = form.cleaned_data['Duration']
            loan.Loan_Start_Date = datetime.datetime.now()
            loan.Loan_End_Date = datetime.date(2035,1,1)
            if loan.Loan_Amount < (credit.Credit_Limit - credit.Current_Balance):
                print("yes")
                loan.Loan_Status = 'ongoing'
                credit.Current_Balance = credit.Current_Balance + loan.Loan_Amount
                loan.save()
                credit.save()
            else:
                loan.Loan_Status = 'cancelled'
                loan.save()
                print("cancelled")
            return render(request,'loan.html' )

    else:
        form = Loan()

    return render(request,'loan.html', {'form': form})

def Loan_repay(request):
    if request.method == 'POST':
        form = Repayment(request.POST)
        if form.is_valid():
            print("yes")
    else:
        form = Repayment()
    return render(request, 'loan_repayment.html', {'form': form})


def credit_card_no(request): 
    n = 6
    range_start = 100**(n - 1)
    range_end = (100**n) - 1
    credit_card_no = random.randint(range_start, range_end)
    print(credit_card_no)
    if request.method == 'POST':
        form = Information(request.POST)
        if form.is_valid():
            info = Personal_Information()
            info.Username = form.cleaned_data['username']
            info.First_Name = form.cleaned_data['firstname']
            info.Last_Name = form.cleaned_data['lastname']
            info.Email = form.cleaned_data['email']
            info.DOB = form.cleaned_data['dob']
            info.Gender = form.cleaned_data['gender']
            info.PAN_Number = form.cleaned_data['pan_number']
            info.PAN_Issue_Date = form.cleaned_data['pan_issue_date']
            info.Aadhar_Number = form.cleaned_data['aadhar_no']
            info.Aadhar_Issue_Date = form.cleaned_data['aadhar_issue_date'] 
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.last_name = form.cleaned_data['lastname']
            user.first_name = form.cleaned_data['firstname']
            user.save()
            info.save()
            application = Application_History()
            userid = info.Username
            application.Username = Personal_Information.objects.get(Username=userid)
            application.Application_Date = datetime.datetime.now()
            print("***********")
            if application.Application_Type == 'Credit Card':
                print("&&&&&&&&&&&&&&&&&&&&&&&&&")
                credit = Credit_Card()
                credit.Username = Personal_Information.objects.get(Username=userid)
                credit.Credit_Card_No = credit_card_no
                credit.Credit_Limit = 50000
                credit.Date_Issued = datetime.datetime.now()
                credit.Date_Expired = datetime.date(2035,1,1)
                credit.Current_Balance = 0
                credit.Rate_Of_Interest = 5
                credit.save()
                application.Status = 'approved'
                application.save()
            return HttpResponseRedirect('loan/')
    else:
        form = Information()

    return render(request,'Credit.html', {'form': form})





        