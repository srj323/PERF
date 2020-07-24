from django import forms

class pay_form(forms.Form):
    Credit_card_no = forms.CharField(label='Credit Card Number')
    username = forms.CharField(label='Name')
    password = forms.CharField(label='Enter your PIN', widget=forms.PasswordInput)
