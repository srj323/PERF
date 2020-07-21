from django.contrib import admin
from .models import Personal_Information,Credit_Card,Contact_Information,Loan_Details,Loan_History,Credit_History,Application_History

admin.site.register(Application_History)

class Personal_Information_Admin(admin.ModelAdmin):
    list_display = ('Username', 'First_Name', 'Last_Name','Email','DOB','Gender','PAN_Number','PAN_Issue_Date','Aadhar_Number','Aadhar_Issue_Date')
admin.site.register(Personal_Information, Personal_Information_Admin)

class Credit_Card_Admin(admin.ModelAdmin):
    list_display = ('Username',
    'Credit_Card_No',
    'Credit_Limit',
    'Date_Issued',
    'Date_Expired',
    'Credit_Card_Status' , #Blocked,Clear
    'Current_Balance',
    'Rate_Of_Interest')
admin.site.register(Credit_Card, Credit_Card_Admin)

class Contact_Information_Admin(admin.ModelAdmin):
    list_display = ('Username', 'Home', 'Street','City','State','Pin','Mobile_Number')
admin.site.register(Contact_Information, Contact_Information_Admin)

class Loan_Details_Admin(admin.ModelAdmin):
    list_display = ('Credit_Card_No','Loan_Type','Loan_Amount','Loan_Duration','Loan_Start_Date','Loan_End_Date','Loan_Status')
admin.site.register(Loan_Details, Loan_Details_Admin)

class Loan_History_Admin(admin.ModelAdmin):
    list_display = ('Payment_Date', 'Payment_Status','Amount_To_Pay','Payment_Paid_On')
admin.site.register(Loan_History, Loan_History_Admin)

class Credit_History_Admin(admin.ModelAdmin):
    list_display = ('Username',
    'Credit_Card_No',
    'Credit_Limit',
    'Balance',
    'Payment_Date')
admin.site.register(Credit_History, Credit_History_Admin)
