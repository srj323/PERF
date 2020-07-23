from django import forms

class Information(forms.Form):
    username = forms.CharField(label='Your name', max_length=100)
    firstname = forms.CharField(label='First name', max_length=100)
    lastname = forms.CharField(label='Last name', max_length=100)
    password = forms.CharField(label='Password', max_length=100,widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    dob = forms.DateField(label='Date Of Birth')
    gender = forms.CharField(label='Gender')
    pan_number = forms.CharField(max_length=100, label='PAN NUMBER')
    pan_issue_date = forms.DateField(label='Pan Issue Date')
    aadhar_no = forms.IntegerField(label='Aadhar NUmber')
    aadhar_issue_date = forms.DateField(label='Aadhar Issue Date')



class Loan(forms.Form):
    Creditcard = forms.IntegerField(label='Credit Card NO')
    Amount = forms.IntegerField(label='Amount Required')
    Duration = forms.IntegerField(label='Time Required to Replay the loan(in months)')


class Repayment(forms.Form):
    Creditcard = forms.IntegerField(label='Credit Card NO')
    username = forms.CharField(label='Your name', max_length=100)
    loan_id = forms.CharField(label='Enter the Load Id you want to')


