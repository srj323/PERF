# Generated by Django 2.1.2 on 2020-03-28 16:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Home', models.CharField(max_length=250)),
                ('Street', models.CharField(max_length=250)),
                ('City', models.CharField(max_length=100)),
                ('State', models.CharField(max_length=100)),
                ('Pin', models.CharField(default=0, max_length=6)),
                ('Mobile_Number', phonenumber_field.modelfields.PhoneNumberField(max_length=13, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='Credit_Card',
            fields=[
                ('Credit_Card_No', models.CharField(max_length=19, primary_key=True, serialize=False)),
                ('Credit_Limit', models.IntegerField()),
                ('Date_Issued', models.DateField()),
                ('Date_Expired', models.DateField()),
                ('Credit_Card_Status', models.CharField(default='Clear', max_length=20)),
                ('Current_Balance', models.FloatField()),
                ('Rate_Of_Interest', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Loan_Details',
            fields=[
                ('Loan_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Loan_Type', models.CharField(max_length=10)),
                ('Loan_Amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('Loan_Duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('Loan_Start_Date', models.DateField()),
                ('Loan_End_Date', models.DateField()),
                ('Loan_Status', models.CharField(max_length=20)),
                ('Credit_Card_No', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cibil.Credit_Card')),
            ],
        ),
        migrations.CreateModel(
            name='Loan_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_Date', models.DateField()),
                ('Payment_Status', models.CharField(max_length=20)),
                ('Amount_To_Pay', models.FloatField()),
                ('Payment_Paid_On', models.DateField()),
                ('Loan_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cibil.Loan_Details')),
            ],
        ),
        migrations.CreateModel(
            name='Personal_Information',
            fields=[
                ('Username', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('First_Name', models.CharField(max_length=30)),
                ('Last_Name', models.CharField(max_length=30)),
                ('Email', models.EmailField(max_length=254)),
                ('DOB', models.DateField()),
                ('Gender', models.CharField(max_length=1)),
                ('PAN_Number', models.CharField(max_length=255)),
                ('PAN_Issue_Date', models.DateField()),
                ('Aadhar_Number', models.CharField(max_length=255)),
                ('Aadhar_Issue_Date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='credit_card',
            name='Username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cibil.Personal_Information'),
        ),
        migrations.AddField(
            model_name='contact_information',
            name='Username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cibil.Personal_Information'),
        ),
    ]
