from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['quiz', 'participant', 'comment', 'content']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Write your main feedback here...'}),
            'content': forms.Textarea(attrs={'placeholder': 'Additional details (optional)...'}),
        }
