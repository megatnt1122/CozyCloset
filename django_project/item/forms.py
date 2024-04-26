from django import forms
from .models import Item


INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'
class NewItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('category', 'size', 'shoeSize', 'name', 'description', 'price', 'image',)

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'size': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'shoeSize': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'size', 'shoeSize', 'description', 'price', 'image', 'is_sold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'size': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'shoeSize': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }