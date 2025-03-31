from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(NHIFClaim)
admin.site.register(NHIFClaimDocument)
admin.site.register(ExcelData)
admin.site.register(Entry)
admin.site.register(InpatientInvoice)
admin.site.register(Patient)
admin.site.register(RenalDialysisRecord)
admin.site.register(Preauthorization)
admin.site.register(DischargeRecord)
admin.site.register(DailySummary)
admin.site.register(DailyTally)

