from cProfile import label
from django import forms

from .models import Comment, Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
      
        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Comment'}
        widgets = {
            'text': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Digite seu comentario'
                })
        }
