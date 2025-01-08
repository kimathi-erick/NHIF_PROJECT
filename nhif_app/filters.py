import django_filters
from .models import NHIFClaim

class NHIFClaimFilter(django_filters.FilterSet):
    done = django_filters.BooleanFilter(widget=django_filters.widgets.BooleanWidget())
    class Meta:
        model = NHIFClaim
        fields = ['nhif_number', 'patient_name', 'procedure', 'dr_code', 'amount', 'status', 'done', 'date']
