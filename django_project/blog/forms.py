from django import forms
from .models import *

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['top', 'bottoms', 'footwear', 'accessory', 'outerwear']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['top'].queryset = userClothes.objects.filter(category__category='Tops', bloguser=user)
            self.fields['bottoms'].queryset = userClothes.objects.filter(category__category='Bottoms', bloguser=user)
            self.fields['footwear'].queryset = userClothes.objects.filter(category__category='Footwear', bloguser=user)
            self.fields['accessory'].queryset = userClothes.objects.filter(category__category='Accessory', bloguser=user)
            self.fields['outerwear'].queryset = userClothes.objects.filter(category__category='Outerwear', bloguser=user)

class DirectMessagingForm(forms.ModelForm):
    class Meta:
        model = ConvoMessage
        fields = ['content',]
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }