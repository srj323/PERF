from django.urls import path
from . import views


urlpatterns = [
    path('credit/', views.credit_card_no,name="Credit_Card"),

]