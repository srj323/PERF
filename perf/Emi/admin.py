from django.contrib import admin
from .models import Emi_Details


class Emi_Details_Admin(admin.ModelAdmin):
    list_display = ('Loan_Id', 'Emi_Duration', 'Interest_Rate','Payment_Status','Amount_To_Pay')
admin.site.register(Emi_Details, Emi_Details_Admin)
