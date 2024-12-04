from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'Ваш email'}),
            'text': forms.Textarea(attrs={'class': 'form__textarea', 'placeholder': 'Ваш комментарий'}),
        }
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'text': 'Комментарий',
        }

    def clean(self):
        cleaned_data = super().clean()
        if not all(cleaned_data.values()):
            raise forms.ValidationError("Все поля должны быть заполнены!")
        return cleaned_data
