from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'Message',
        }

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
