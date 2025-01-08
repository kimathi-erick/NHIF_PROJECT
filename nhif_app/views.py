from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from .filters import NHIFClaimFilter
from django.http import HttpResponseRedirect, HttpResponse,FileResponse,JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q,Sum
from PIL import Image, ImageDraw, ImageFont
import io
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import tempfile
from datetime import datetime
from django.templatetags.static import static
import base64
from django.http import FileResponse, Http404
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
import pandas as pd
from django.db import transaction
from openpyxl import Workbook
from PyPDF2 import PdfReader, PdfWriter,PageObject,PdfMerger
from reportlab.pdfgen import canvas
from openpyxl.styles import Font, Alignment
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader 
import math
from docx import Document
import openpyxl
import os
import fitz
import PyPDF2
from django.core.files.storage import FileSystemStorage


def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('icd11_browser')  # Change 'home' to the name of your homepage view
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'nhif_app/login.html', {'form': form})



@login_required
def claim_list(request):
    claims = NHIFClaim.objects.all()
    claim_filter = NHIFClaimFilter(request.GET, queryset=claims)
    query_params = request.GET.copy()
    if 'done' in query_params and query_params['done'] == 'true':
        query_params['done'] = True
    else:
        query_params['done'] = False
    filtered_claims = claim_filter.qs

    context = {
        'claim_filter': claim_filter,
        'filtered_claims': filtered_claims,
        'status_choices': NHIFClaim.STATUS_CHOICES,
        'doctor_choices': NHIFClaim.DOCTOR_CHOICES,
    }
    return render(request, 'nhif_app/claim_list.html', context)
@login_required
def claim_detail(request, pk):
    claim = get_object_or_404(NHIFClaim, pk=pk)
    documents = claim.documents.all()
    if request.method == 'POST':
        form = NHIFClaimDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.claim = claim
            document.save()
            return HttpResponseRedirect(reverse('document_list', args=[pk]))
    else:
        form = NHIFClaimDocumentForm()
    return render(request, 'nhif_app/claim_detail.html', {'claim': claim, 'documents': documents, 'form': form})
@login_required
def claim_create(request):
    if request.method == 'POST':
        form = NHIFClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('claim_list')
    else:
        form = NHIFClaimForm()
    return render(request, 'nhif_app/claim_form.html', {'form': form})
@login_required
def claim_update(request, pk):
    claim = get_object_or_404(NHIFClaim, pk=pk)
    if request.method == 'POST':
        form = NHIFClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('claim_detail', pk=claim.pk)
    else:
        form = NHIFClaimForm(instance=claim)
    return render(request, 'nhif_app/claim_form.html', {'form': form})
@login_required
def claim_delete(request, pk):
    claim = get_object_or_404(NHIFClaim, pk=pk)
    if request.method == 'POST':
        claim.delete()
        return redirect('claim_list')
    return render(request, 'nhif_app/claim_confirm_delete.html', {'claim': claim})
@login_required
def upload_document(request, pk):
    claim = get_object_or_404(NHIFClaim, pk=pk)
    if request.method == 'POST':
        form = NHIFClaimDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.claim = claim
            document.save()
            return HttpResponseRedirect(reverse('document_list', args=[pk]))
    else:
        form = NHIFClaimDocumentForm()
    return render(request, 'nhif_app/upload_document.html', {'form': form, 'claim': claim})
@login_required
def document_list(request, pk):
    claim = get_object_or_404(NHIFClaim, pk=pk)
    documents = claim.documents.all()
    
    # Search filter
    search_query = request.GET.get('search', '')
    if search_query:
        documents = documents.filter(Q(document_name__icontains=search_query))
    
    # Pagination
    paginator = Paginator(documents, 10)  # Show 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'nhif_app/document_list.html', {'claim': claim, 'documents': page_obj})
@login_required
def document_download(request, document_id):
    document = get_object_or_404(NHIFClaimDocument, id=document_id)
    response = HttpResponse(document.document, content_type='application/pdf')  # Adjust content_type if needed
    response['Content-Disposition'] = f'attachment; filename="{document.document_name}"'
    return response
@login_required
def document_delete(request, document_id):
    document = get_object_or_404(NHIFClaimDocument, id=document_id)
    claim_pk = document.claim.pk  # Retrieve claim pk
    if request.method == 'POST':
        document.delete()
        return redirect('document_list', pk=claim_pk)
    return redirect('document_list', pk=claim_pk)

@login_required
def surgical_receipt(request):
    if request.method == 'POST':
        # Existing receipt calculation logic
        procedure_cost = float(request.POST.get('procedure_cost', 0))
        has_implant = request.POST.get('has_implant') == 'on'
        implant_cost = float(request.POST.get('implant_cost', 0)) if request.POST.get('implant_cost') else 0
        admission_fee = 1000

        if has_implant:
            remaining_cost = procedure_cost - implant_cost - admission_fee
        else:
            remaining_cost = procedure_cost - admission_fee

        if remaining_cost < 0:
            remaining_cost = 0

        surgeon_fee = remaining_cost * 0.30
        anaesthetic_fee = remaining_cost * 0.15
        theatre_fees = remaining_cost * 0.20
        laboratory_fees = remaining_cost * 0.10
        pharmacy_fees = remaining_cost * 0.10
        daily_charges_fee = remaining_cost * 0.15

        total_fees = (
            admission_fee + surgeon_fee + anaesthetic_fee + theatre_fees +
            laboratory_fees + pharmacy_fees + daily_charges_fee
        )

        if has_implant:
            total_fees += implant_cost

        current_date = datetime.now().strftime('%Y-%m-%d')

        # Context without the stamp_image
        context = {
            'procedure_cost': procedure_cost,
            'implant_cost': implant_cost,
            'has_implant': has_implant,
            'admission_fee': admission_fee,
            'surgeon_fee': surgeon_fee,
            'anaesthetic_fee': anaesthetic_fee,
            'theatre_fees': theatre_fees,
            'laboratory_fees': laboratory_fees,
            'pharmacy_fees': pharmacy_fees,
            'daily_charges_fee': daily_charges_fee,
            'total_fees': total_fees,
            'current_date': current_date,
        }

        return render(request, 'nhif_app/receipt.html', context)

    return render(request, 'nhif_app/receipt_form.html')

@login_required
def entry_list(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'diary/entry_list.html', {'entries': entries})

@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'diary/entry_detail.html', {'entry': entry})
@login_required
def entry_new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # Link the entry to the current user
            entry.save()
            return redirect('entry_list')
    else:
        form = EntryForm()
    return render(request, 'diary/entry_edit.html', {'form': form})
@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            return redirect('entry_list')
    else:
        form = EntryForm(instance=entry)
    return render(request, 'diary/entry_edit.html', {'form': form})
@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == "POST":
        entry.delete()
        return redirect('entry_list')
    return render(request, 'diary/entry_confirm_delete.html', {'entry': entry})
@login_required
def calculate_billing(request):
    if request.method == 'POST':
        form = MorgueBillingForm(request.POST)
        if form.is_valid():
            billing = form.save()
            total_cost = billing.calculate_total()
            return render(request, 'nhif_app/billing_result.html', {'total_cost': total_cost, 'billing': billing})
    else:
        form = MorgueBillingForm()
    
    return render(request, 'nhif_app/billing_form.html', {'form': form})
@login_required
def filter_data(request):
    form = FilterForm(request.GET or None)
    results = ExcelData.objects.none()  # Default to an empty queryset

    if form.is_valid():
        cleaned_data = form.cleaned_data
        filter_args = {}

        if cleaned_data['ClaimNumber']:
            filter_args['ClaimNumber__icontains'] = cleaned_data['ClaimNumber']
        if cleaned_data['MemberNumber']:
            filter_args['MemberNumber__icontains'] = cleaned_data['MemberNumber']
        if cleaned_data['PatientNumber']:
            filter_args['PatientNumber__icontains'] = cleaned_data['PatientNumber']
        if cleaned_data['PatientName']:
            filter_args['PatientName__icontains'] = cleaned_data['PatientName']
        if cleaned_data['Stage']:
            filter_args['Stage__icontains'] = cleaned_data['Stage']    

        if filter_args:
            results = ExcelData.objects.filter(**filter_args).only(
                'ClaimNumber', 'AdmissionDate', 'DischargeDate', 'Stage',
                'MemberNumber', 'DependentNumber', 'PatientNumber', 'PatientName',
                'InvoiceNumber', 'ExpectedClaim', 'ClaimDate', 'ChequeNumber',
                'ChequeDate', 'EFTTransactionNumber', 'EFTBatchNo'
            )

    # Apply pagination to results
    paginator = Paginator(results, 20)  # Show 20 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'nhif_app/filter_results.html', {
        'form': form, 
        'page_obj': page_obj, 
    })
@login_required    
def delete_excel_data(request):
    if request.method == 'POST':  # Ensure it's a POST request to avoid accidental deletion
        ExcelData.objects.all().delete()
        return redirect('filter_data')  # Redirect to a success page or another URL
    return HttpResponse('Invalid request method.', status=405)
@login_required
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Load the Excel file into a DataFrame, skipping the first row
            file = request.FILES['file']
            df = pd.read_excel(file, skiprows=1)  # Skip the first row

            # Clean column headers: remove spaces and join multiple words
            df.columns = df.columns.str.replace(' ', '', regex=False)

            # Prepare a list of ExcelData objects for bulk insertion
            entries = [
                ExcelData(
                    ClaimNumber=row['ClaimNumber'],
                    AdmissionDate=row['AdmissionDate'],
                    DischargeDate=row['DischargeDate'],
                    Stage=row['Stage'],
                    MemberNumber=row['MemberNumber'],
                    DependentNumber=row['DependentNumber'],
                    PatientNumber=row['PatientNumber'],
                    PatientName=row['PatientName'],
                    InvoiceNumber=row['InvoiceNumber'],
                    ExpectedClaim=row['ExpectedClaim'],
                    ClaimDate=row['ClaimDate'],
                    ChequeNumber=row['ChequeNumber'],
                    ChequeDate=row['ChequeDate'],
                    EFTTransactionNumber=row['EFTTransactionNumber'],
                    EFTBatchNo=row['EFTBatchNo'],
                ) for _, row in df.iterrows()
            ]

            # Use a transaction to ensure all rows are inserted together
            with transaction.atomic():
                ExcelData.objects.bulk_create(entries)

            return render(request, 'nhif_app/upload_success.html')

    else:
        form = UploadFileForm()

    return render(request, 'nhif_app/upload.html', {'form': form})
@login_required    
def create_invoice(request):
    if request.method == 'POST':
        form = InpatientInvoiceForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            invoice = form.save()

            # Call the calc method to calculate the fees
            calculated_fees = invoice.calc()

            # Pass the calculated fees to the template
            return render(request, 'nhif_app/invoice_result.html', {'calculated_fees': calculated_fees, 'invoice': invoice})
    else:
        form = InpatientInvoiceForm()

    return render(request, 'nhif_app/create_invoice.html', {'form': form})
@login_required    
def dialysis_management(request):
    if request.method == 'POST':
        form = PatientExportForm(request.POST)
        action = request.POST.get('action')  # Detect which button was clicked

        if form.is_valid():
            selected_date = form.cleaned_data['date']
            selected_patients = form.cleaned_data['patients']
            claim_amount = 10650  # Set the claim amount

            if action == 'save':
                # Save records logic
                for patient in selected_patients:
                    # Check if the record already exists for the selected patient and date
                    if not RenalDialysisRecord.objects.filter(patient=patient, date_of_admission=selected_date).exists():
                        RenalDialysisRecord.objects.create(
                            patient=patient,
                            date_of_admission=selected_date,
                            date_of_discharge=selected_date,
                            claim_amount=claim_amount
                        )
                messages.success(request, 'Records saved successfully.')
                return redirect('dialysis_management')

            elif action == 'generate_excel':
                # Fetch records for the selected date
                records = RenalDialysisRecord.objects.filter(date_of_admission=selected_date)

                if not records:
                    messages.warning(request, f'No records found for {selected_date}.')
                    return redirect('dialysis_management')

                # Create Excel workbook and sheet
                workbook = Workbook()
                sheet = workbook.active
                sheet.title = 'Renal Dialysis Records'

                # Add merged heading
                sheet.merge_cells('A1:I1')
                sheet['A1'] = f'Renal Dialysis Records - {selected_date}'
                sheet['A1'].font = Font(size=14, bold=True)
                sheet['A1'].alignment = Alignment(horizontal='center', vertical='center')

                # Add headers
                headers = [
                    'Date of Admission', 'Date of Discharge', 'Patient Name',
                    'Shif Number', 'Service Rendered', 'Facility Name',
                    'ID Number', 'Phone Number', 'Claim Amount'
                ]
                sheet.append(headers)

                # Add patient records
                for record in records:
                    sheet.append([
                        record.date_of_admission.strftime('%Y-%m-%d'),
                        record.date_of_discharge.strftime('%Y-%m-%d'),
                        record.patient.name,
                        record.patient.shifnumber,
                        record.patient.service,
                        record.patient.facility_name,
                        record.patient.idnumber,
                        record.patient.phone,
                        record.claim_amount
                    ])

                # Prepare the response for download
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                filename = f"renal_dialysis_records_{selected_date}.xlsx"
                response['Content-Disposition'] = f'attachment; filename={filename}'

                # Save the workbook to the response
                workbook.save(response)
                return response
    else:
        form = PatientExportForm()

    return render(request, 'nhif_app/dialysis_management.html', {'form': form})
@login_required
def create_update_patient(request, pk=None):
    patient = get_object_or_404(Patient, pk=pk) if pk else None

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('create_patient')  # Redirect to create_patient after saving
    else:
        form = PatientForm(instance=patient)

    patients = Patient.objects.all()  # Retrieve all patients
    return render(request, 'nhif_app/patient_form.html', {
        'form': form,
        'patient': patient,
        'patients': patients,
    })
@login_required
def print_claim_form(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    # Ensure the patient has an associated claim form
    if not patient.claim_form:
        raise Http404("No claim form uploaded for this patient.")

    # Serve the file as a response
    response = FileResponse(patient.claim_form.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{patient.claim_form.name}"'  # 'inline' for viewing in browser, 'attachment' for download
    return response
@login_required    
def stage_summary(request):
    # Query to group by 'Stage' and sum the 'ExpectedClaim' field
    stage_totals = (
        ExcelData.objects
        .values('Stage')
        .annotate(total_claim=Sum('ExpectedClaim'))
        .order_by('Stage')
    )

    return render(request, 'nhif_app/stage_summary.html', {'stage_totals': stage_totals})
@login_required  
def icd11_view(request):
    return render(request, 'nhif_app/icd11_page.html')

@login_required 
def merge_documents(request):
    return render(request, 'nhif_app/merge_documents.html')
@login_required 
def pdf_form_view(request):
    return render(request, 'nhif_app/pdf_form.html')
@login_required     
def preauthorization_form(request):
    if request.method == "POST":
        form = PreauthorizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stage_summary")  # Replace with your success page URL or name
    else:
        form = PreauthorizationForm()
    return render(request, "nhif_app/preauthorization_form.html", {"form": form})

# View for listing preauthorizations
@login_required 
def preauthorization_list(request):
    query = request.GET.get('q')
    preauthorizations = Preauthorization.objects.all().order_by('-id')
    if query:
        preauthorizations = preauthorizations.filter(
            Q(patient_name__icontains=query) | 
            Q(doctor_name__icontains=query) |
            Q(procedure__icontains=query)
        )  
    return render(request, 'nhif_app/preauthorization_list.html', {
        'preauthorizations': preauthorizations,
        'query': query,
    })
@login_required 
def preauthorization_edit(request, pk):
    preauthorization = get_object_or_404(Preauthorization, pk=pk)
    
    if request.method == 'POST':
        form = PreauthorizationForm(request.POST, instance=preauthorization)
        if form.is_valid():
            form.save()
            return redirect('preauthorization_list')  # Redirect to the list after saving
    else:
        form = PreauthorizationForm(instance=preauthorization)  # Pre-populate form with existing data
    
    return render(request, 'nhif_app/preauthorizationedit_form.html', {
        'form': form,
        'preauthorization': preauthorization,
        'is_editing': True  # Flag to indicate editing
    })
@login_required 
def preauthorization_delete(request, pk):
    preauthorization = get_object_or_404(Preauthorization, pk=pk)
    if request.method == 'POST':
        preauthorization.delete()
        return redirect('preauthorization_list')
    return render(request, 'nhif_app/preauthorization_confirm_delete.html', {
        'preauthorization': preauthorization
    })