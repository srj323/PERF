from django.urls import path, re_path, include

from . import views

urlpatterns = [
    # path('/score', views.get_cibil_score, name='Cibil_Score'),
    path('info/', views.emi_calculation, name='Emi_Info'),
]
