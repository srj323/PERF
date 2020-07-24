from djongo import models
from Cibil.models import *
# Create your models here.
class Emi_Details(models.Model):
    Loan_Id =  models.ForeignKey(Loan_Details, on_delete=models.CASCADE)
    Emi_Duration = models.IntegerField(validators=[MinValueValidator(0)])
    Interest_Rate = models.FloatField()
    Payment_Status = models.CharField(max_length=20)
    Amount_To_Pay = models.FloatField()
    Curr_Emi_Amount = models.FloatField()
    Curr_Interest_Amount = models.FloatField()
    Curr_Closing_Amount = models.FloatField()
