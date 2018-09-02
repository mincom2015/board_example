from django import forms
from .models import Board, Topic, Post


class TopicNewForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
                              max_length=4000,
                              help_text="The max length of the text is 4000.",
                              required=True)

    class Meta:
        model = Topic
        fields = ['subject', 'message']
