from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class NHIFClaim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('approved', 'Approved'),
    ]
    DOCTOR_CHOICES = [
    ('A4157', 'Kariuki'),
    ('A5027', 'Mugendi'),
    ('A3655', 'Chira'),
    ('A14254', 'Akampa'),
    ('013033', 'Adong'),
    ('A7642', 'Kaguongo'),
    ('A4653', 'Nderitu'),
    ('A6843', 'Amandi'),
    ('A7489', 'Laichena'),
    ('A10231', 'Okendi'),
    ('A6253', 'Sung'),
    ('A9479', 'Naomi'),
    ('A8245', 'Mutiso'),
    ('A9347', 'Milo'),
    ]


    nhif_number = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=100)
    procedure = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    dr_code = models.CharField(max_length=20, choices=DOCTOR_CHOICES, default='none')
    done = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.patient_name} - {self.procedure}"

class NHIFClaimDocument(models.Model):
    claim = models.ForeignKey('NHIFClaim', on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=255)
    document = models.FileField(upload_to='nhif_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} for {self.claim.nhif_number}"


class MorgueBilling(models.Model):
    BODY_TYPES = [
        ('outside', 'Outside Hospital'),
        ('inside', 'Inside Hospital'),
    ]

    AGE_GROUPS = [
        ('adult', 'Adult'),
        ('child', 'Child'),
    ]

    body_type = models.CharField(max_length=10, choices=BODY_TYPES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUPS, default='adult')
    body_income_date = models.DateField(default=timezone.now)
    body_release_date = models.DateField(null=True, blank=True)

    def calculate_total(self):
        # Initialize default costs
        preparation_cost = 0
        sheet_cost = 0

        if self.body_type == 'outside':
            preparation_cost = 2000
            sheet_cost = 500 if self.age_group == 'adult' else 250
        elif self.body_type == 'inside':
            preparation_cost = 1500
            sheet_cost = 500 if self.age_group == 'adult' else 250

        # Calculate days in the morgue
        days_in_morgue = self.calculate_days_in_morgue()

        # Calculate cost based on days in the morgue
        if days_in_morgue <= 7:
            days_cost = days_in_morgue * 500
        else:
            days_cost = (7 * 500) + ((days_in_morgue - 7) * 600)

        # Total cost calculation
        total_cost = preparation_cost + sheet_cost + days_cost
        return total_cost

    def calculate_days_in_morgue(self):
        if self.body_release_date:
            delta = self.body_release_date - self.body_income_date
            return max(delta.days, 0)
        return 0

    def __str__(self):
        return f"Body Type: {self.get_body_type_display()} | Age Group: {self.get_age_group_display()} | Days: {self.calculate_days_in_morgue()}"
class ExcelData(models.Model):
    ClaimNumber = models.CharField(max_length=255)
    AdmissionDate = models.CharField(max_length=255)
    DischargeDate = models.CharField(max_length=255)
    Stage = models.CharField(max_length=255)
    MemberNumber = models.CharField(max_length=255)
    DependentNumber = models.CharField(max_length=255)
    PatientNumber = models.CharField(max_length=255)
    PatientName = models.CharField(max_length=255)
    InvoiceNumber = models.CharField(max_length=255)
    ExpectedClaim = models.CharField(max_length=255)
    ClaimDate = models.CharField(max_length=255)
    ChequeNumber = models.CharField(max_length=255)
    ChequeDate = models.CharField(max_length=255)
    EFTTransactionNumber = models.CharField(max_length=255)
    EFTBatchNo = models.CharField(max_length=255)

class InpatientInvoice(models.Model):
    ApprovedAmount = models.FloatField()
    AccumulatedBill = models.FloatField()
    Procedure = models.CharField(max_length=255)
    ImplantCheck = models.BooleanField(default=False)

    def calc(self):
        # Calculate the remainder after accounting for accumulated bill
        Remainder = self.ApprovedAmount - self.AccumulatedBill

        if self.ImplantCheck:
            # Adjusted percentages when there is an implant (must add to 1.0)
            surgeon_fee = Remainder * 0.30
            anaesthetic_fee = Remainder * 0.10
            theatreExpenses = Remainder * 0.20
            procedureamount = Remainder * 0.25
            implantcharges = Remainder * 0.15  # Applied when implant is present
        else:
            # Adjusted percentages when there is no implant (must add to 1.0)
            surgeon_fee = Remainder * 0.35
            anaesthetic_fee = Remainder * 0.15
            theatreExpenses = Remainder * 0.20
            procedureamount = Remainder * 0.30
            implantcharges = 0  # No implant charges if ImplantCheck is False

        # Return the calculated values
        return {
            'surgeon_fee': surgeon_fee,
            'anaesthetic_fee': anaesthetic_fee,
            'theatreExpenses': theatreExpenses,
            'procedureamount': procedureamount,
            'implantcharges': implantcharges
        }

class Patient(models.Model):
    name = models.CharField(max_length=100)
    shifnumber = models.CharField(max_length=50)  # Replacing member_number with shifnumber
    service = models.CharField(default="Dialysis", max_length=100)
    facility_name = models.CharField(default="Our Lady Of Lourdes Mwea Hospital",max_length=100)  # New field for name of facility
    idnumber = models.CharField(max_length=50)  # New field for ID number
    phone = models.CharField(max_length=15)  # New field for phone number
    claim_form = models.FileField(upload_to='claim_forms/', null=True, blank=True)

    def __str__(self):
        return self.name

class RenalDialysisRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_admission = models.DateField(default=timezone.now)
    date_of_discharge = models.DateField(default=timezone.now)  # Same as date_of_admission
    claim_amount = models.DecimalField(default=10650, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.patient.name} - {self.claim_amount}"

    # Overriding save to ensure both dates are the same and claim_amount is set
    def save(self, *args, **kwargs):
        if not self.date_of_admission:
            self.date_of_admission = timezone.now()
        self.date_of_discharge = self.date_of_admission  # Set discharge equal to admission
        if not self.claim_amount:
            self.claim_amount = 9500
        super().save(*args, **kwargs)

class Preauthorization(models.Model):
    patient_name = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=255)
    procedure = models.CharField(max_length=255)
    expected_surgery_date = models.DateField()
    chief_complaint = models.TextField()
    vital_signs = models.TextField()
    hpi = models.TextField(help_text="History of present illness")
    physical_examination = models.TextField()
    investigation_report_details = models.TextField()

    ANAESTHESIA_CHOICES = [
        ("general", "General Anaesthesia"),
        ("local", "Local Anaesthesia"),
        ("spinal", "Spinal Block"),
        ("sedation", "Sedation"),
    ]
    type_of_anaesthesia = models.CharField(max_length=50, choices=ANAESTHESIA_CHOICES)

    is_condition_related_to_employment = models.BooleanField(default=False)
    is_condition_related_to_accident = models.BooleanField(default=False)
    is_patient_co_insured = models.BooleanField(default=False)

    def __str__(self):
        return f"Preauth for {self.patient_name} - {self.procedure} on {self.expected_surgery_date}"
WARD_TYPE_CHOICES = [
    ('ICU/HDU', 'ICU/HDU'),
    ('Medical', 'Medical'),
    ('Surgical', 'Surgical'),
    ('Amenity', 'Amenity'),
    ('Maternity', 'Maternity'),
    ('Gynecology', 'Gynecology'),
    ('Pediatrics', 'Pediatrics'),
]

class DischargeRecord(models.Model):
    number = models.IntegerField(primary_key=True, null=False)
    patient_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_admission = models.DateField()
    date_of_discharge = models.DateField()
    inpatient_number = models.CharField(max_length=20)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPE_CHOICES)
    claim_number = models.CharField(max_length=20, editable=False)
    days_spent = models.PositiveIntegerField(editable=False)
    amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
    # Set `number` to the highest value + 1 (auto-increment)
        if self.number is None:
            last_record = DischargeRecord.objects.aggregate(Max('number'))
            self.number = (last_record['number__max'] or 0) + 1

        # Calculate days spent
        self.days_spent = (self.date_of_discharge - self.date_of_admission).days

        # Save the object first to auto-generate the `number`
        super().save(*args, **kwargs)

        # After the object is saved, generate the claim number using the `number` field
        year_month = self.date_of_discharge.strftime('%Y%m')
        self.claim_number = f"{year_month}{int(self.number):03d}"  # Ensure `self.number` is an integer

        # Save the updated claim number to the database
        super().save(update_fields=['claim_number'])
class DailySummary(models.Model):
    patient_name = models.CharField(max_length=100)
    id_no = models.CharField(max_length=20)
    doa = models.DateField()
    dod = models.DateField(null=True, blank=True)  # Allow null and blank
    diagnosis = models.TextField()
    procedure_plan = models.TextField()
    mobile_number = models.CharField(max_length=15)

class DailyTally(models.Model):
    date = models.DateField(default=date.today)
    admissions = models.IntegerField()
    discharges = models.IntegerField()
    surgeries = models.IntegerField()
    deliveries = models.IntegerField()
    radiology = models.IntegerField()
    referrals_in = models.IntegerField()
    referrals_out = models.IntegerField()

