from django import forms

from customers.models import Customer
from leads.models import Lead

from .models import Opportunity


class OpportunityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(status='active')
        self.fields['lead'].queryset = Lead.objects.exclude(status='converted')

    class Meta:
        model = Opportunity
        fields = [
            'title',
            'customer',
            'lead',
            'stage',
            'value',
            'probability',
            'expected_close_date',
            'loss_reason',
            'notes',
        ]
        widgets = {
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        stage = cleaned_data.get('stage')
        loss_reason = (cleaned_data.get('loss_reason') or '').strip()
        customer = cleaned_data.get('customer')
        lead = cleaned_data.get('lead')

        if not customer and not lead:
            raise forms.ValidationError('Select at least a customer or a lead.')

        if stage == 'closed_lost' and not loss_reason:
            self.add_error('loss_reason', 'Loss reason is required for closed lost opportunities.')

        if stage != 'closed_lost':
            cleaned_data['loss_reason'] = ''

        return cleaned_data
