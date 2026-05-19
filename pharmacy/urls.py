from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.add_medicine, name='add_medicine'),
    path('medicines/edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('medicines/delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
    path('billing/', views.billing, name='billing'),
    path('billing/generate/', views.generate_bill, name='generate_bill'),
    path('sales/', views.sales_history, name='sales_history'),
]