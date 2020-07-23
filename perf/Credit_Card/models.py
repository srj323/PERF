from django.db import models

# Create your models here.

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    Credit_Card_No = models.CharField(max_length=40)
    Loan_Id =  models.CharField(max_length=40)
    amount = models.IntegerField(default=0)
    razorpayid = models.CharField(max_length=255,default="")
    razorpaypaymentid = models.CharField(max_length=255,default="")
    razorpaysignature = models.CharField(max_length=255, default="")