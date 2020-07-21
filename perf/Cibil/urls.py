from django.urls import path, re_path, include

from . import views

urlpatterns = [
    # path('/score', views.get_cibil_score, name='Cibil_Score'),
    path('info/', views.get_all_info, name='Cibil_Info'),
    path('score/', views.get_cibil, name = 'Cibil_Score')
]
