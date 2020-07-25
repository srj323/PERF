from django.shortcuts import render
from dateutil.relativedelta import relativedelta
from datetime import datetime,date,timedelta
from Cibil.models import *
from .models import *
import schedule
import time
from threading import Thread
from django.core.mail import send_mail
# def every_monday_morning():
#     print("This is run every Monday morning at 7:30")
#
# import time
#
# def job():
#     print("I'm working...")
#
# # schedule.every(1).minutes.do(job)
# # schedule.every().hour.do(job)
# schedule.every().day.at("00:22").do(job)

# while 1:
#     schedule.run_pending()
#     time.sleep(1)
# Create your views here.





def numOfDays(date1, date2):
    return (date2-date1).days

def emi(p, r, t):

    r = r/(100*12)
    interest_amt = (p*r)

    # for one month period
    t = t
    emi = round((p*r*(1+r)**t)/(((1+r)**t)-1))

    #Principle amt paid
    closing_balance = round(p - (emi-interest_amt))

    return emi,round(interest_amt,2),closing_balance

def emi_days(p, r, t, days):
    #input:
        #principal(p)
        #rate(r) per annum
        #duration(t) in days
        #days :for which you need to find emi,interest and closing balance
    # for one month interest
    r = r/(100*365)
    interest_amt = (p*r*days)

    # for one month period
    t = t
    emi = round(((p*r*(1+r)**t)/(((1+r)**t)-1))*days)

    #Principle amt paid
    closing_balance = round(p - (emi-interest_amt))

    return emi,round(interest_amt,2),closing_balance

#check wheather card is blocked before calling this function(handel by loan person)
def start_emi(Loan_Id):
    #INPUT : Loan_Id = Loan_Details Object

    payment_date = Loan_Id.Loan_Start_Date + relativedelta(months=1)
    payment_date = payment_date.replace(day=1) - relativedelta(days=1)
    days = numOfDays(Loan_Id.Loan_Start_Date,payment_date+relativedelta(days=1))
    print("days=",days)
    duration = numOfDays(Loan_Id.Loan_Start_Date, Loan_Id.Loan_End_Date)
    emi_amt,interest_amt,closing_balance = emi_days(Loan_Id.Loan_Amount, Loan_Id.Loan_Interest_Rate, duration,days)
    Emi_Details.objects.create(Loan_Id=Loan_Id, Emi_Duration=Loan_Id.Loan_Duration, Interest_Rate=Loan_Id.Loan_Interest_Rate,Payment_Status="ongoing",Amount_To_Pay=Loan_Id.Loan_Amount, Curr_Emi_Amount=emi_amt,Curr_Interest_Amount=interest_amt, Curr_Closing_Amount=closing_balance)
    Loan_History.objects.create(Loan_Id=Loan_Id, Payment_Date=payment_date, Payment_Status="ongoing", Amount_To_Pay=emi_amt)
    credit_card = Credit_Card.objects.get(Credit_Card_No=Loan_Id.Credit_Card_No)
    print("old_balace=",credit_card.Current_Balance)
    credit_card.Current_Balance = credit_card.Current_Balance + emi_amt
    credit_card.save()
    print("new_balace=",credit_card.Current_Balance)
    mail = Loan_Id.Credit_Card_No.Username.Email
    mail_subject = 'PERF: EMI Update'
    message = f'Your EMI for this month against Loan Id:{Loan_Id.Loan_Id} is {emi_amt}. Last date to pay you EMI is payment_date'
    send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])


def update_emi():
    if date.today().day != 1:
        return
    print("Starting monthly emi_update....")
    emi_list = Emi_Details.objects.filter(Payment_Status="ongoing")
    print(emi_list)
    for emi_info in emi_list:
        loan_id = emi_info.Loan_Id
        loan = Loan_History.objects.get(Loan_Id=loan_id, Payment_Date=date.today()-relativedelta(days=1))
        if loan.Payment_Status=="completed":
            p = emi_info.Curr_Closing_Amount
            r = emi_info.Interest_Rate
            t = emi_info.Emi_Duration
            if p>0:
                if t>0:
                    emi_amt,interest_amt,closing_balance = emi(p,r,t)
                    payment_date = date.today() + relativedelta(months=1)
                    payment_date = payment_date.replace(day=1) - relativedelta(days=1)
                    Loan_History.objects.create(Loan_Id=loan_id, Payment_Date=payment_date, Payment_Status="ongoing", Amount_To_Pay=emi_amt)
                    card_obj = loan_id.Credit_Card_No
                    curr_balance = card_obj.Current_Balance
                    card_obj.Current_Balance=curr_balance+emi_amt
                    card_obj.save()
                    emi_info.Emi_Duration=t-1
                    emi_info.Amount_To_Pay = p
                    emi_info.Curr_Emi_Amount = emi_amt
                    emi_info.Curr_Interest_Amount = interest_amt
                    emi_info.Curr_Closing_Amount = closing_balance
                    emi_info.save()
                    mail = loan_id.Credit_Card_No.Username.Email
                    mail_subject = 'PERF: EMI Update'
                    message = f"Your EMI for this month against Loan Id:{Loan_Id.Loan_Id} is {emi_amt}, "
                    send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                else:
                    emi_info.Amount_To_Pay = p
                    emi_info.Curr_Emi_Amount = 0
                    emi_info.Curr_Interest_Amount = 0
                    emi_info.Curr_Closing_Amount = 0
                    if emi_info.Payment_Status=="unrecovered":
                        emi_info.Payment_Status="recovered"
                    else:
                       emi_info.Payment_Status="completed"
                    mail = loan_id.Credit_Card_No.Username.Email
                    mail_subject = 'PERF: EMI Update'
                    message = f"Your Loan for Loan Id:{Loan_Id.Loan_Id} is completed"
                    send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                    emi_info.save()

            else:
                 emi_info.Amount_To_Pay = p
                 emi_info.Curr_Emi_Amount = 0
                 emi_info.Curr_Interest_Amount = 0
                 emi_info.Curr_Closing_Amount = 0
                 if emi_info.Payment_Status=="unrecovered":
                     emi_info.Payment_Status="recovered"
                 else:
                    emi_info.Payment_Status="completed"
                 mail = loan_id.Credit_Card_No.Username.Email
                 mail_subject = 'PERF: EMI Update'
                 message = f"Your Loan for Loan Id:{Loan_Id.Loan_Id} is completed"
                 send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])
                 emi_info.save()

        elif loan.Payment_Status=="ongoing":
            loan.Payment_Status="unrecovered"
            loan.save()
            p = emi_info.Amount_To_Pay
            r = emi_info.Interest_Rate
            t = emi_info.Emi_Duration
            if p>0:
                if t>0:
                    emi_amt,interest_amt,closing_balance = emi(p,r,t)
                    payment_date = date.today() + relativedelta(months=1)
                    payment_date = payment_date.replace(day=1) - relativedelta(days=1)
                    Loan_History.objects.create(Loan_Id=loan_id, Payment_Date=payment_date, Payment_Status="ongoing", Amount_To_Pay=emi_amt)
                    card_obj = loan_id.Credit_Card_No
                    curr_balance = card_obj.Current_Balance
                    card_obj.Current_Balance = curr_balance + emi_amt - emi_info.Curr_Emi_Amount
                    card_obj.save()
                    emi_info.Emi_Duration=t-1
                    emi_info.Amount_To_Pay = p
                    emi_info.Curr_Emi_Amount = emi_amt
                    emi_info.Curr_Interest_Amount = interest_amt
                    emi_info.Curr_Closing_Amount = closing_balance
                    emi_info.save()
                    mail = loan_id.Credit_Card_No.Username.Email
                    mail_subject = 'PERF: EMI Update'
                    message = f"You have not paid you EMI for previous month.So, now your EMI has been changed. Your EMI for Loan Id:{Loan_Id.Loan_Id} is {emi_amt}"
                    send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])

                else:
                    emi_amt,interest_amt,closing_balance = emi(p,r,0)
                    payment_date = date.today() + relativedelta(months=1)
                    payment_date = payment_date.replace(day=1) - relativedelta(days=1)
                    Loan_History.objects.create(Loan_Id=loan_id, Payment_Date=payment_date, Payment_Status="ongoing", Amount_To_Pay=emi_amt)
                    card_obj = loan_id.Credit_Card_No
                    curr_balance = card_obj.Current_Balance
                    card_obj.Current_Balance = curr_balance + emi_amt - emi_info.Curr_Emi_Amount
                    card_obj.save()
                    emi_info.Emi_Duration=0
                    emi_info.Amount_To_Pay = p
                    emi_info.Curr_Emi_Amount = emi_amt
                    emi_info.Curr_Interest_Amount = interest_amt
                    emi_info.Curr_Closing_Amount = closing_balance
                    emi_info.save()
                    mail = loan_id.Credit_Card_No.Username.Email
                    mail_subject = 'PERF: EMI Update'
                    message = f"You have not paid you EMI for previous month.So, now your EMI has been changed. Your EMI for Loan Id:{Loan_Id.Loan_Id} is {emi_amt}"
                    send_mail(mail_subject, message, 'perf.mail.mail@gmail.com', [mail])






def emi_calculation(request):
    principal_amount = 40000;
    rate_of_interest = 12;
    loan_duration = 3;# in months
    credit_card = Credit_Card.objects.get(Credit_Card_No="1234567890123456789")
    Loan_Id = Loan_Details.objects.get(Credit_Card_No=credit_card, Loan_Status="ongoing", Loan_Amount=40000.0,On_Emi=True)
    duration = numOfDays(Loan_Id.Loan_Start_Date, Loan_Id.Loan_End_Date)
    print("duration",duration)
    start_emi(Loan_Id)
    days = 8
    emi_info,interest_amt,closing_balance = emi_days(principal_amount, rate_of_interest, duration,days);
    print("Monthly EMI is= ", emi_info,interest_amt,closing_balance)
    principal_amount = closing_balance
    while(principal_amount > 0):
        emi_info,interest_amt,closing_balance = emi(principal_amount, rate_of_interest, loan_duration);
        print("Monthly EMI is= ", emi_info,interest_amt,closing_balance)
        principal_amount = closing_balance
        loan_duration -= 1


def scheduler():
    schedule.every().day.at("00:22").do(update_emi)

    while 1:
         schedule.run_pending()
         time.sleep(60)

background_thread = Thread(target=scheduler)
background_thread.start()
