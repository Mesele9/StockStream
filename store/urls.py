# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Item URLs
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    
    # Purchase Record URLs
    path('purchase-records/', views.purchase_record_list, name='purchase_record_list'),
    path('purchase-records/new/', views.purchase_record_create, name='purchase_record_create'),
    path('purchase-records/<int:pk>/', views.purchase_record_detail, name='purchase_record_detail'),
    path('purchase/<int:pk>/edit/', views.purchase_record_edit, name='purchase_record_edit'),
    path('purchase/<int:pk>/delete/', views.purchase_record_delete, name='purchase_record_delete'),

    
    # Issue Record URLs
    path('issue-records/', views.issue_record_list, name='issue_record_list'),
    path('issue-records/new/', views.issue_record_create, name='issue_record_create'),
    path('issue-records/<int:pk>/', views.issue_record_detail, name='issue_record_detail'),
    path('issue/<int:pk>/edit/', views.issue_record_edit, name='issue_record_edit'),
    path('issue/<int:pk>/delete/', views.issue_record_delete, name='issue_record_delete'),
    
    # Other URLs can be added here
]

