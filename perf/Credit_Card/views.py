from django.shortcuts import render
from django.http import HttpResponseRedirect
from Cibil.models import Credit_Card, Personal_Information, Application_History, Loan_Details, Loan_History, Contact_Information
import random
from .forms import Information, Loan, Repayment, log_form
from Cibil.views import extract_cibil
from Emi.views import start_emi, emi
from dateutil.relativedelta import relativedelta
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail
from django.contrib import admin
from django.template.loader import render_to_string

import razorpay
razorpay_client = razorpay.Client(auth=("rzp_test_HjTkiDCGJADmpE", "FFuLbceQq7d3bxsL2rawq6oR"))


# Create your views here.
def index(request):
    return render(request, 'index.html')
    
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
            payment_date = loan.Loan_Start_Date + relativedelta(months=loan.Loan_Duration+1)
            payment_date = payment_date.replace(day=1) - relativedelta(days=1)
            loan.Loan_End_Date = payment_date
            usern = credit.Username
            h = Personal_Information.objects.get(Username=usern)
            print(h)
            mail = h.Email
            if loan.Loan_Amount < (credit.Credit_Limit - credit.Current_Balance):
                print("yes")
                loan.Loan_Status = 'ongoing'
                print(credit.Current_Balance)
                print(credit.Credit_Limit - credit.Current_Balance)
                credit.Current_Balance = credit.Current_Balance + loan.Loan_Amount
                option = form.cleaned_data['option']
                print(option)
                loan.save()
                credit.save()
                if option == True :
                    start_emi(loan)
                    print(loan)
                    emi_amt,interest,closing_bal = emi(loan.Loan_Amount,credit.Rate_Of_Interest,loan.Loan_Duration)
                    if emi_amt + credit.Current_Balance < credit.Credit_Limit : 
                        loan.On_Emi = True
                        loan.save()
                        mail_subject = 'Loan PERF'
                        message = 'Loan has been approved over EMI'
                        send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                    else:
                        mail_subject = 'Loan PERF'
                        message = 'Loan has been cancelled as your cant do it over EMI'
                        send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                        loan.Loan_Status = 'cancelled'
                        loan.save()

                else:
                    mail_subject = 'Loan PERF'
                    message = 'Loan has been approved!!'
                    send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                    loan.save()
                    
            else:
                mail_subject = 'Loan PERF'
                message = 'Loan has been cancelled.'
                send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
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
            number = form.cleaned_data['Creditcard']
            name = form.cleaned_data['username']
            loanid = form.cleaned_data['loan_id']
            detail = Loan_Details.objects.filter(Loan_Id=loanid)
            print(detail)
            for i in detail:
                amount = i.Loan_Amount
                print(amount)
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'
            notes = {'name': name}
            razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
            print(razorpay_order['id'])
            order = Orders(Loan_Id=loanid, Credit_Card_No=number, amount=amount, razorpayid=razorpay_order['id'])   # saving in dataset just like by using python as in shell
            order.save()
            return render(request, 'payment.html', {'order_id': razorpay_order['id'], 'cname': name, 'cemail': number,'cphone':loanid})

    else:
        form = Repayment()
    return render(request, 'loan_repayment.html', {'form': form})


def app_charge(request):
    if request.method == "POST":
        try:
            print("yeah")
            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            print(order_id)
            signature = request.POST.get('razorpay_signature','')
            print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            order_db = Orders.objects.get(razorpayid=order_id)
            order_db.razorpaypaymentid = payment_id
            order_db.razorpaysignature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                print("2nd")
                amount = order_db.amount*100
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    thank = True
                    print("here")
                    # id = request.POST.get('shopping_order_id','')
                    # p = OrderUpdate.objects.order_by('order_id').last()
                    # id = p.order_id
                    params = {'thank': thank}
                    update = Orders.objects.get(razorpayid=order_id)
                    no = update.Credit_Card_No
                    print(no)
                    loanidd = update.Loan_Id
                    print(loanidd)
                    update_d = Credit_Card.objects.get(Credit_Card_No=no)
                    update_d.Current_Balance = max(update_d.Current_Balance - order_db.amount,0)
                    update_d.save()
                    update_dd = Loan_Details.objects.get(Loan_Id=loanidd)
                    update_dd.Loan_Amount = update_dd.Loan_Amount - order_db.amount
                    update_dd.Loan_Status = 'completed'
                    update_dd.Loan_End_Date = datetime.datetime.now()
                    update_dd.save()
                    # response = json.dumps(razorpay_client.payment.fetch(payment_id))
                    return render(request, 'loan_repayment.html', params)
                except:
                    print("expect")
                    thank =  False
                    return render(request, 'loan_repayment.html', {'thank': thank})
            else:
                print("else")
                thank =  False
                return render(request, 'loan_repayment.html', {'thank': thank})
        except:
            thank =  False
            return render(request, 'loan_repayment.html', {'thank': thank})


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
            contact = Contact_Information()
            contact.Home = form.cleaned_data['Home']
            contact.Street = form.cleaned_data['Street']
            contact.City = form.cleaned_data['City']
            contact.State = form.cleaned_data['State']
            contact.Pin = form.cleaned_data['Pin']
            contact.Mobile_Number = form.cleaned_data['Mobile_Number']
            
            contact.save()
            user = authenticate(username=username, password=password)
            print("**********8")
            if user is not None:
                print("************")
                info.save()
                application = Application_History()
                userid = info.Username
                application.Username = Personal_Information.objects.get(Username=userid)
                application.Application_Date = datetime.datetime.now()
                contact.Username = Personal_Information.objects.get(Username=userid)
                contact.save()
                print("***********")
                if application.Application_Type == 'Credit Card':
                    credit = Credit_Card()
                    credit.Username = Personal_Information.objects.get(Username=userid)
                    n = len(Credit_Card.objects.filter(Username=credit.Username))
                    if n < 3 :
                        credit.Credit_Card_No = credit_card_no
                        if extract_cibil(userid) == "Not Enough Credit History" :
                            credit.Credit_Limit = 10000
                            credit.Date_Issued = datetime.datetime.now()
                            credit.Date_Expired = datetime.date(2035,1,1)
                            credit.Current_Balance = 0
                            credit.Rate_Of_Interest = 5
                            credit.save()
                            application.Status = 'approved'
                            application.save()
                        elif int(extract_cibil(userid)) < 499 :
                            credit.Credit_Limit = 30000
                            credit.Date_Issued = datetime.datetime.now()
                            credit.Date_Expired = datetime.date(2035,1,1)
                            credit.Current_Balance = 0
                            credit.Rate_Of_Interest = 5
                            credit.save()
                            application.Status = 'approved'
                            application.save()
                        elif int(extract_cibil(userid)) < 600 :
                            credit.Credit_Limit = 50000
                            credit.Date_Issued = datetime.datetime.now()
                            credit.Date_Expired = datetime.date(2035,1,1)
                            credit.Current_Balance = 0
                            credit.Rate_Of_Interest = 5
                            credit.save()
                            application.Status = 'approved'
                            application.save()
                        elif int(extract_cibil(userid)) <= 660 :
                            credit.Credit_Limit = 70000
                            credit.Date_Issued = datetime.datetime.now()
                            credit.Date_Expired = datetime.date(2035,1,1)
                            credit.Current_Balance = 0
                            credit.Rate_Of_Interest = 5
                            credit.save()
                            application.Status = 'approved'
                            application.save()
                        elif int(extract_cibil(userid)) <= 780 :
                            credit.Credit_Limit = 100000
                            credit.Date_Issued = datetime.datetime.now()
                            credit.Date_Expired = datetime.date(2035,1,1)
                            credit.Current_Balance = 0
                            credit.Rate_Of_Interest = 5
                            credit.save()
                            application.Status = 'approved'
                            application.save()
                        else:
                            credit.Credit_Limit = 120000
                            credit.Date_Issued = datetime.datetime.now()
                            credit.Date_Expired = datetime.date(2035,1,1)
                            credit.Current_Balance = 0
                            credit.Rate_Of_Interest = 5
                            credit.save()
                            application.Status = 'approved'
                            application.save()
                    else:
                        application.Status = 'rejected'
                        application.save()
                        messages.success(request, f'Your are exceding the maximum Credit Card')


                messages.success(request, f'Your account has been successfully created')

            else:
                
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
                    contact.Username = Personal_Information.objects.get(Username=userid)
                    contact.save()
                    credit.Credit_Card_No = credit_card_no
                    
                    credit.Credit_Limit = 50000
                    credit.Date_Issued = datetime.datetime.now()
                    credit.Date_Expired = datetime.date(2035,1,1)
                    credit.Current_Balance = 0
                    credit.Rate_Of_Interest = 5
                    credit.save()
                    application.Status = 'approved'
                    application.save()
                messages.success(request, f'Your account has been successfully created')
    else:
        form = Information()

    return render(request,'Credit.html', {'form': form})





def log(request):
    if request.method == 'POST':
        form = log_form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("**********************")
                personal_info = Personal_Information.objects.get(Username=username)
                card = Credit_Card.objects.filter(Username=personal_info.Username)
                # print(card.Credit_Card_No)
                print(card)
                # lon = Loan_Details.objects.filter(Credit_Card_No=card.Credit_Card_No)
                # print(lon)
                return render(request, 'profile1.html', {'personal_info':personal_info, 'card':card})
            else:
                return render(request, 'login.html')
    
    else:
        form = log_form()
    
    return render(request, 'login.html',{'form':form})