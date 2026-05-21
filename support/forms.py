from django import forms
from .models import SupportTicket, TicketComment


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['customer', 'issue_type', 'subject', 'description', 'priority', 'status', 'assigned_to']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'issue_type': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'})
        }
        labels = {
            'body': 'Comment'
        }