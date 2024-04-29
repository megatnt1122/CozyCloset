from django import forms
from .models import *
from django import forms
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from .models import Post

class PostForm(forms.ModelForm):
    item_image = forms.URLField(label='Item Image URL', required=False)  # Add a URL field for the item image

    class Meta:
        model = Post
        fields = ['content']  # Remove 'image' field from the form

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Get the item image URL from the form data
        item_image_url = self.cleaned_data.get('item_image', '')

        if item_image_url:
            # Download the image from the URL and save it to a temporary file
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(item_image_url).read())
            img_temp.flush()

            # Save the temporary image file to the instance's image field
            instance.image.save(f"{instance.pk}_image.jpg", File(img_temp), save=False)

        if commit:
            instance.save()
        return instance

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
            'body': forms.Textarea(attrs={
                'class': 'form-control', 
                'style': 'min-height: 80px; width: 100%;',  # Add this line
                'placeholder': 'Type your comment here...'
            })
        }
