from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import surgical_receipt
from django.contrib.auth.views import LogoutView
from .views import custom_login_view,create_update_patient

urlpatterns = [
    path('login/', custom_login_view, name='login'),  # Custom login view
    path('logout/', LogoutView.as_view(), name='logout'),  # Built-in LogoutView
    path('', views.claim_list, name='claim_list'),
    path('claim/<int:pk>/', views.claim_detail, name='claim_detail'),
    path('claim/new/', views.claim_create, name='claim_create'),
    path('claim/<int:pk>/edit/', views.claim_update, name='claim_update'),
    path('claim/<int:pk>/delete/', views.claim_delete, name='claim_delete'),
    path('claim/<int:pk>/upload/', views.upload_document, name='upload_document'),
    path('claim/<int:pk>/documents/', views.document_list, name='document_list'),
    path('document/download/<int:document_id>/', views.document_download, name='document_download'),
    path('document/delete/<int:document_id>/', views.document_delete, name='document_delete'),
    path('surgical-receipt/', surgical_receipt, name='surgical_receipt'),
    path('entrylist/', views.entry_list, name='entry_list'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/new/', views.entry_new, name='entry_new'),
    path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('billing/', views.calculate_billing, name='calculate_billing'),
    path('filter/', views.filter_data, name='filter_data'),
    path('upload/', views.upload_file, name='upload_file'),
    path('create-invoice/', views.create_invoice, name='create_invoice'),
    path('delete-excel-data/', views.delete_excel_data, name='delete_excel_data'),
    path('dialysis-management/', views.dialysis_management, name='dialysis_management'),
    path('patients/create/', create_update_patient, name='create_patient'),  # Route for creating a patient
    path('patients/update/<int:pk>/', create_update_patient, name='update_patient'),  # Route for updating a patient
    path('stage-summary/', views.stage_summary, name='stage_summary'),
    path('icd11/', views.icd11_view, name='icd11_browser'),
    path('merge_documents/', views.merge_documents, name='document_merge'),
    path('pdf-form/', views.pdf_form_view, name='pdf_form'),
    path('patient/<int:pk>/print_claim_form/', views.print_claim_form, name='print_claim_form'),
    path('preauthorization/', views.preauthorization_form, name='preauthorization_form'),
    path('preauthorizations/', views.preauthorization_list, name='preauthorization_list'),  # List view
    path('preauthorizations/edit/<int:pk>/', views.preauthorization_edit, name='preauthorization_edit'),  # Edit view
    path('preauthorizations/delete/<int:pk>/', views.preauthorization_delete, name='preauthorization_delete'),  # Delete view
    

   
]
