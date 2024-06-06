from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm
from ckeditor.widgets import CKEditorWidget
from django import forms


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']  # Include fields for author and text
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    # Override the __init__ method to set placeholder text
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.TextInput(attrs={'placeholder': 'Your name'})
        self.fields['text'].widget = forms.Textarea(attrs={'placeholder': 'Your comment'})


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)