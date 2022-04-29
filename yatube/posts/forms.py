from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)
        labels = {
            'text': ('Сообщение'),
            'group': ('Группа'),
        }
        help_texts = {
            'text': ('Введите сообщение'),
            'group': ('Выберите группу'),
        }
