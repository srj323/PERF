from django.shortcuts import render
from django.http import HttpResponseRedirect
from Cibil.models import Credit_Card, Personal_Information, Application_History
import random
from .forms import *
import datetime
from django.utils import timezone




# Create your views here.
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
            info.save()
            application = Application_History()
            application.Username = Personal_Information.objects.latest('Username')
            application.Application_Date = datetime.datetime.now()
            print("***********")
            if application.Application_Type == 'Credit Card':
                print("&&&&&&&&&&&&&&&&&&&&&&&&&")
                credit = Credit_Card()
                credit.Username = Personal_Information.objects.latest('Username')
                credit.Credit_Card_No = credit_card_no
                credit.Credit_Limit = 50000
                credit.Date_Issued = datetime.datetime.now()
                credit.Date_Expired = datetime.datetime.now()
                credit.Current_Balance = 0
                credit.Rate_Of_Interest = 5
                credit.save()
                application.Status = 'approved'
                application.save()
            return HttpResponseRedirect('/application')
    else:
        form = Information()

    return render(request,'Credit.html', {'form': form})


        