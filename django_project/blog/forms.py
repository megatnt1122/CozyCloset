from django import forms
from .models import *
from django import forms
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from .models import Post

class SingleLineTextField(forms.CharField):
    widget = forms.TextInput

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

    def __init__(self, *args, **kwargs):
        shareditem = kwargs.pop('shareditem', None)
        super(PostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) and not isinstance(field.widget, forms.Textarea):
                field.widget = forms.TextInput()
        if shareditem:
            self.fields['image'].initial = shareditem.image
            self.fields['image'].widget = forms.HiddenInput()  # Hide the image field when shareditem is present


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
    
    def __init__(self, *args, **kwargs):
        super(DirectMessagingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) and not isinstance(field.widget, forms.Textarea):
                field.widget = forms.TextInput()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.CharField) and not isinstance(field.widget, forms.Textarea):
                field.widget = forms.TextInput()
