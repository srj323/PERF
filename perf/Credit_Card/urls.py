from django.urls import path
from . import views


urlpatterns = [
    path("credit/", views.credit_card_no,name="Credit_Card"),
    path("loan/", views.Loan_no, name="Loan"),
    # path("loan_repayment/", views.Loan_repay, name="Loanrepayment"),
    path("payment/", views.Loan_repay,name="payment"),
    path("payment/charge/", views.app_charge,name="charge")

]