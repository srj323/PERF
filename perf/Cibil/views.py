from django.shortcuts import render
from .models import *

from datetime import date

def numOfDays(date1, date2):
    return (date2-date1).days

# Create your views here.
def calculateScoreOnAge(age,usage_age):   #AGE IN YEARS
    if (age <2):
        print("Insufficient Credit History")
        return 0
    else : return (0.15*min(850,((age-usage_age)*6+(usage_age)*18+300)))//1 #for every 3 years
#	if (age <= 3) : return 45
#   if (age <= 5): return 55
#   if (age <= 10): return 75
#   if (age <= 15): return 95
#   if (age <= 20): return 105
#   if (age <=25) : return 125
#   if (age >25) : return 135

def calculateScoreOnHomeOwnership(ownership):
    if (ownership == 'own'):
        return 225
    else:
        return 110

############################

def ScoreOnHistory(loan_list):
    total_nof_loans = sum(loan_list)
    if total_nof_loans!=0:
        nof_loans_paidontime = loan_list[0]
        nof_loans_within30 = loan_list[1]
        nof_loans_within60 = loan_list[2]
        nof_loans_within90 = loan_list[3]
        nof_loans_after90 = loan_list[4]
        return (110)*(nof_loans_paidontime*5 + nof_loans_within30*3 + nof_loans_within60*2 + nof_loans_within90*1 + nof_loans_after90*-2)/(total_nof_loans)
    else:
        return 0

def calculateScoreOnHistory(loan_details):
    list = [0]*5
    for card in loan_details:
        for loan in card:
            if loan[0].Loan_Status == 'completed':
                a = numOfDays(loan[0].Loan_End_Date,date.today())/365 #in years i.e convert days to years
                recent_factor = 1/(1+(a//7))# for every slab of 7 years
                x = numOfDays(loan[0].Loan_Start_Date,loan[0].Loan_End_Date)-loan[0].Loan_Duration
                if x==0: list[0]+=recent_factor*1
                elif x>90: list[4]+=recent_factor*1
                elif x>60: list[3]+=recent_factor*1
                elif x>30: list[2]+=recent_factor*1
                else: list[1]+=recent_factor*1
    score = ScoreOnHistory(list)

	#not_paid = -1
	#on_time = 5
	#within_x_days = 4-(x//30)
	# if x>90: paid_ontime=-2
	# elif x==0: paid_ontime=5
	# else: paid_ontime = 3-(x//30)
    his_score = max(0,score)+300  # 105 is the bias or min score
    final_score = 0.35 * min(850, his_score)
    return final_score//1


def ratio_factor(ratio):   #more credit hungry you are higher the risk is associated
    if ratio==0: return 0
    elif ratio<=10: return 4
    elif ratio<=30: return 3
    elif ratio<=50: return 2
    elif ratio<=80: return -1
    else: return -2


def utilization_score(credit_limit,loan_amt,credit_issue_date):
    recent_factor = 1/(1+(numOfDays(credit_issue_date,date.today())//365*7))
    ratio = (loan_amt/credit_limit)*100
    score = (recent_factor*ratio_factor(ratio))
    return score

def calculateScoreOnAmtOwed(score):
    return 0.3*min(850,(300+score))  #min(90)-max(270)


def calculateScoreOnNewCredit(username):
    application_list = Application_History.objects.filter(Username=username)
    credit_count = len(Credit_Card.objects.filter(Username=username))
    score = 0
    if credit_count>0:
        if len(application_list)>0:
            for application in application_list:
                if (date.today()-application.Application_Date).days<=365:
                    score+=150;
        score*=credit_count

    return 0.1*max(300,850-score)




def calculateScoreOnIncome(income):
    if (income <= 10000): return 120
    if (income <= 25000): return 140
    if (income <= 35000): return 180
    if (income <= 50000): return 200
    if (income > 50000): return 225


def calculateCreditScore(age,homeOwnership,income,usage_age):
    return calculateScoreOnAge(age,usage_age)+calculateScoreOnHomeOwnership(homeOwnership)+ calculateScoreOnIncome(income)


def calculateCreditRating(score):
    if (score >= 800): return 'Exceptional'
    if (score >= 740): return 'Very Good'
    if (score >= 670): return 'Good'
    if (score >= 580): return 'Average'
    if (score >= 300): return 'Poor'
    else: return 'Limited/No Credit'






def calculateLoanThreshold(rating):
    if(rating == 'Average'): return 30000
    if(rating == 'Good'): return 40000
    if(rating == 'Very Good'): return 50000
    if(rating == 'Great'): return 70000
    else: return 0


def calculateInterest(rating):
    if(rating == 'Average'): return 24.7
    if(rating == 'Good'): return 18.9
    if(rating == 'Very Good'): return 13.39
    if(rating == 'Great'): return 6.99
    else: return 29.99


def createCalculation(loan, limit, term, interest):
    useLoan = loan
    if(loan > limit):
        useLoan = limit

    totalInterest = (interest * useLoan * term) / 100
    totalRepayment = totalInterest + useLoan
    monthlyRepayment = totalRepayment / (term * 12)
    return {
        'approvedLoan': useLoan,
        'monthlyRepayment': monthlyRepayment,
        'totalRepayment': totalRepayment ,
        'totalInterest': totalInterest
    }


age=31
homeOwnership='own'
income=5000000
loanAmount=100000
type='personal'
usage_age=0

creditScore = calculateCreditScore(age,homeOwnership,income,usage_age);
creditRating = calculateCreditRating(creditScore);
loanThreshold = calculateLoanThreshold(creditRating);
approvedInterest = calculateInterest(creditRating);

granted = 'DENIED';
if (creditScore > 490):
    granted = 'ACCEPTED'
    result = {'creditScore': creditScore,
            'creditRating': creditRating,
            'approval': granted,
            'loanThreshold': loanThreshold,
            'interest': approvedInterest,
            'calculation': {
                'threeYear': createCalculation(loanAmount, loanThreshold, 3, approvedInterest),
                'fiveYear': createCalculation(loanAmount, loanThreshold, 5, approvedInterest),
                }
            }
    print(result)
else:
        result = {
            'creditScore': creditScore,
            'creditRating': creditRating,
            'approval': granted
        }
        print(result)





###################################################



def get_cibil(credit_card_list,details,personal_info):
    age_score=0
    credit_utilization_score = 0
    for card in credit_card_list:
        age = numOfDays(card.Date_Issued,min(date.today(),card.Date_Expired))/365 #------------------------------------------------->for calculating score by age

        loan_details_list = Loan_Details.objects.filter(Credit_Card_No=card.Credit_Card_No)

        usage_age=0 #--------------------------------------------------------------------------------------------->for calculating score by age
        loan_amt = 0

        for loan in loan_details_list:
            usage_age += numOfDays(loan.Loan_Start_Date,min(date.today(),loan.Loan_End_Date))/365#---------------------------------->for calculating score by age
            # loan_amt += loan.Loan_Amount
        age_score+= calculateScoreOnAge(age,usage_age)#----------------------------------------------------------->for calculating score by age

        utilization_history = Credit_History.objects.filter(Credit_Card_No=card.Credit_Card_No)
        utilization_score_ = 0
        for history in utilization_history:
            credit_limit,loan_amt,credit_issue_date = history.Credit_Limit,history.Balance,history.Payment_Date
            utilization_score_ += utilization_score(credit_limit,loan_amt,credit_issue_date)
        credit_utilization_score += calculateScoreOnAmtOwed(utilization_score_)

    history_score = calculateScoreOnHistory(details)
    new_credit_score = calculateScoreOnNewCredit(personal_info)
    aa = len(credit_card_list)
    bb = len(credit_card_list)
    if aa==0:
        aa+=1
    if bb==0:
        bb+=1
    final_credit_score = (age_score//aa) + (credit_utilization_score//bb) + history_score + new_credit_score
    # print("age_score",'----->',age_score//len(credit_card_list))#----------------------------------------------------->for calculating score by age
    # print("Credit Utilization score",'----->',credit_utilization_score//len(credit_card_list))
    # print("History score",'----->',history_score)
    # print("new_credit_score",'--------->',new_credit_score)
    print("Total Score","--------->",final_credit_score)
    if age_score//aa>0:
        return final_credit_score
    else:
        return  "Not Enough Credit History"



def get_all_info(request):
    personal_info = Personal_Information.objects.get(Username='srj2')
    contact_info = Contact_Information.objects.get(Username=personal_info)
    credit_card_list = Credit_Card.objects.filter(Username = personal_info)
    # loan_details_list = []
    # loan_history_list = []
    details = []


    for card in credit_card_list:
        loan_details = Loan_Details.objects.filter(Credit_Card_No=card)                 #[Loan_Details [loan_card[loan_item[loan][loan_history[][]]]]]
        loan_card = []
        for loan in loan_details:
            history=[]
            loan_item = []
            loan_item.append(loan)
            history = Loan_History.objects.filter(Loan_Id=loan)
            loan_item.append(history)
            loan_card.append(loan_item)
        details.append(loan_card)
    print("---------------------cibil-score------------------------")
    credit_score = get_cibil(credit_card_list,details,personal_info)
    # print(details)
    # for card in details:
    #     for loan_item in card:
    #         print(loan_item[0])
    #         for history in loan_item[1]:
    #             print(history)




    # for card in credit_card_list:
    #     loan_details_list.append(Loan_Details.objects.filter(Credit_Card_No=card))
    #
    # for loan_details in loan_details_list:
    #     loan_history = []
    #     for loan in loan_details:
    #         loan_history.append(Loan_History.objects.filter(Loan_Id=loan))
    #     loan_history_list.append(loan_history)
    #
    #
    # for loan in loan_details_list:
    #     for i in loan:
    #         print(i)



    # print("--------------------Personal Information-----------------------------------")
    # print();print()
    # print("Username: ",end=" ");print(personal_info.Username)
    # print("Name: ",end=" ");print(personal_info.First_Name+ " " + personal_info.Last_Name)
    # print("Email: ",end=" "); print(personal_info.Email)
    # print("DOB: ",end=" "); print(personal_info.DOB)
    # print("Gender: ",end=" "); print(personal_info.Gender)
    # print();print();print()
    # print("--------------------------Identity Proof---------------------")
    # print();print()
    # print("PAN_Number: ",end=" "); print(personal_info.PAN_Number,end="                 "); print("PAN_Issue_Date: ",end=" "); print(personal_info.PAN_Issue_Date)
    # print("Aadhar_Number: ",end=" "); print(personal_info.Aadhar_Number,end="                 "); print("Aadhar_Issue_Date: ",end=" "); print(personal_info.Aadhar_Issue_Date)
    # print();print();print()
    # print("--------------------------Contact Informatuon-------------------------")
    # print();print()
    # print("Address: ",end=" ");print(contact_info.Home + ", " + contact_info.Street + ", " + contact_info.City + ", " + contact_info.State)
    # print("PIN: ",end=" ");print(contact_info.Pin)
    # print("Mobile Number: ",end=" ");print(contact_info.Mobile_Number)
    # print();print();print()
    # print()
    return render(request, 'profile.html',{'personal_info': personal_info, 'contact_info': contact_info, 'credit_card_list':credit_card_list, 'details':details,'credit_score':credit_score})


    # return render(request, 'Doctor/time_slots.html', context=context)











#####################################################
