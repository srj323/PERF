# Generated by Django 2.1.2 on 2020-07-23 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cibil', '0004_auto_20200723_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emi_details',
            name='Loan_Id',
        ),
        migrations.DeleteModel(
            name='Emi_Details',
        ),
    ]
