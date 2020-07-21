#
# from django.contrib.auth.models import User
# from djongo import models
# from phonenumber_field.modelfields import PhoneNumberField
# from django.core.validators import MinValueValidator, MaxValueValidator
#
#
# Identification_Type_CHOICES = (
#     ('Income Tax ID Number(PAN)', 'Income Tax ID Number(PAN)'),
#     ('Aadhar Number', 'Aadhar Number'),
# )
#
#
# class Personal_Information(models.Model):
#     Username = models.CharField(primary_key=True,max_length=255)
#     First_Name = models.CharField(max_length=30)
#     Last_Name = models.CharField(max_length=30)
#     Email = models.EmailField()
#     DOB = models.DateField()
#     Gender = models.CharField(max_length=1)
#     Credit_Card_No = models.CharField(max_length=19)
#     PAN_Number = models.CharField(max_length=255)
#     PAN_Issue_Date = models.DateField()
#     PAN_Expiration_Date = models.DateField()
#     Aadhar_Number = models.CharField(max_length=255)
#     Aadhar_Issue_Date = models.DateField()
#
#     def __str__(self):
#         return self.Username
#
# class Credit_Card(models.Model):
#     Credit_Card_No = models.CharField(primary_key=True,max_length=19)
#     Credit_Limit = models.IntegerField()
#     Date_Issued = models.DateField()
#     Date_Expired = models.DateField()
#     Credit_Card_Status = models.CharField(max_length=20,default='Clear') #Blocked,Clear
#     Current_Balance = models.FloatField()
#     Rate_Of_Interest = models.FloatField()
#
#
#
# class Contact_Information(models.Model):
#
#     Home = models.CharField(max_length=250)
#     Street = models.CharField(max_length=250)
#     City = models.CharField(max_length=100)
#     State = models.CharField(max_length=100)
#     Pin = models.CharField(max_length=6,default=000000)
#     Mobile_Number = PhoneNumberField(max_length=13)
#
# class Loan_Details(models.Model):
#     Loan_Id = models.AutoField(primary_key=True)
#     Credit_Card_No = models.ForeignKey(Credit_Card, on_delete=models.CASCADE)
#     Loan_Type = models.CharField(max_length=10)
#     Loan_Amount = models.FloatField(validators=[MinValueValidator(0)])
#     Loan_Duration = models.IntegerField(validators=[MinValueValidator(0)]) #in DAYS
#     Loan_Start_Date = models.DateField()
#     Loan_End_Date = models.DateField() # will be updated when loan is completed
#     Loan_Status = models.CharField(max_length=20) #ongoing,completed,cancelled,UnRecovered.
#
# class Loan_History(models.Model):
#     Loan_Id =  models.ForeignKey(Loan_Details, on_delete=models.CASCADE)
#     Payment_Date = models.DateField()
#     Payment_Status = models.CharField(max_length=20)
#     Amount_To_Pay = models.FloatField()
#     #Amount_Paid
