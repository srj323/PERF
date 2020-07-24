from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("credit/", views.credit_card_no,name="Credit_Card"),
    path("loan/", views.Loan_no, name="Loan"),
    # path("loan_repayment/", views.Loan_repay, name="Loanrepayment"),
    path("payment/", views.Loan_repay,name="payment"),
    path("payment/charge/", views.app_charge,name="charge"),
    path("login", views.log,name="Log"),
    path('', views.index)
    

]+ static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)