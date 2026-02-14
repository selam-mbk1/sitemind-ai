# chat/forms.py

from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Ask something about your documents..."
        }),
        label=""
    )
