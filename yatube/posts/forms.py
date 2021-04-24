<<<<<<< HEAD
from django.forms import ModelForm, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'group': 'Группа',
            'text': 'Текст',
            'image': 'Изображение'
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        labels = {'text': 'Текст'}
        widgets = {'text': Textarea(attrs={'rows': 4})}
=======
from django.forms import ModelForm, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        labels = {
            'group': 'Группа',
            'text': 'Текст',
            'image': 'Изображение'
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        labels = {'text': 'Текст'}
        widgets = {'text': Textarea(attrs={'rows': 4})}
>>>>>>> e00ceddaa1758d008aea9fd3ff70b76728ca2368
