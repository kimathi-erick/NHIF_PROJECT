from django import forms
from .models import *
from django.forms.widgets import DateInput

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your entry here...'}),
        }

class NHIFClaimForm(forms.ModelForm):
    class Meta:
        model = NHIFClaim
        fields = ['nhif_number', 'patient_name', 'procedure', 'amount', 'status', 'dr_code', 'date', 'done']
        widgets = {
            'nhif_number': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'procedure': forms.TextInput(attrs={'class': 'form-control'}),
            'dr_code': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Added done field
        }
class NHIFClaimDocumentForm(forms.ModelForm):
    class Meta:
        model = NHIFClaimDocument
        fields = ['document_name', 'document']

class MorgueBillingForm(forms.ModelForm):
    class Meta:
        model = MorgueBilling
        fields = ['body_type', 'age_group', 'body_income_date', 'body_release_date']
        widgets = {
            'body_type': forms.Select(attrs={'class': 'form-control'}),
            'age_group': forms.Select(attrs={'class': 'form-control'}),  # Add age_group field
            'body_income_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'body_release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class FilterForm(forms.Form):
    ClaimNumber = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Claim Number'})
    )
    MemberNumber = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Member Number'})
    )
    PatientNumber = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient Number'})
    )
    PatientName = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient Name'})
    )
    Stage = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Stage Name'})
    )
class InpatientInvoiceForm(forms.ModelForm):
    class Meta:
        model = InpatientInvoice
        fields = ['ApprovedAmount', 'AccumulatedBill', 'Procedure', 'ImplantCheck']
        widgets = {
            'ApprovedAmount': forms.NumberInput(attrs={'class': 'form-control'}),
            'AccumulatedBill': forms.NumberInput(attrs={'class': 'form-control'}),
            'Procedure': forms.TextInput(attrs={'class': 'form-control'}),
            'ImplantCheck': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'ApprovedAmount': 'Approved Amount',
            'AccumulatedBill': 'Accumulated Bill',
            'Procedure': 'Procedure Description',
            'ImplantCheck': 'Has Implant?',
        }
class PatientExportForm(forms.Form):
    patients = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Select Patients'
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Select Date'
    )
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'shifnumber','service','facility_name','idnumber','phone','claim_form']
class PreauthorizationForm(forms.ModelForm):
    class Meta:
        model = Preauthorization
        fields = [
            "patient_name",
            "doctor_name",
            "procedure",
            "expected_surgery_date",
            "chief_complaint",
            "vital_signs",
            "hpi",
            "physical_examination",
            "investigation_report_details",
            "type_of_anaesthesia",
            "is_condition_related_to_employment",
            "is_condition_related_to_accident",
            "is_patient_co_insured",
        ]
        widgets = {
            "patient_name": forms.TextInput(attrs={"class": "form-control"}),
            "doctor_name": forms.TextInput(attrs={"class": "form-control"}),
            "procedure": forms.TextInput(attrs={"class": "form-control"}),
            "expected_surgery_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "chief_complaint": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "vital_signs": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "hpi": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "physical_examination": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "investigation_report_details": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "type_of_anaesthesia": forms.Select(attrs={"class": "form-select"}),
            "is_condition_related_to_employment": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_condition_related_to_accident": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_patient_co_insured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
class DischargeRecordForm(forms.ModelForm):
    class Meta:
        model = DischargeRecord
        fields = ['number','patient_name', 'date_of_birth', 'date_of_admission', 'date_of_discharge',
                  'inpatient_number', 'ward_type', 'amount']
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "patient_name": forms.TextInput(attrs={"class": "form-control"}),
            "inpatient_number": forms.TextInput(attrs={"class": "form-control"}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_admission': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_discharge': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ward_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class DailySummaryForm(forms.ModelForm):
    class Meta:
        model = DailySummary
        fields = '__all__'
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_no': forms.TextInput(attrs={'class': 'form-control'}),
            'doa': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dod': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': False}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control','rows': 2}),
            'procedure_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DailyTallyForm(forms.ModelForm):
    class Meta:
        model = DailyTally
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'admissions': forms.NumberInput(attrs={'class': 'form-control'}),
            'discharges': forms.NumberInput(attrs={'class': 'form-control'}),
            'surgeries': forms.NumberInput(attrs={'class': 'form-control'}),
            'deliveries': forms.NumberInput(attrs={'class': 'form-control'}),
            'radiology': forms.NumberInput(attrs={'class': 'form-control'}),
            'referrals_in': forms.NumberInput(attrs={'class': 'form-control'}),
            'referrals_out': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

