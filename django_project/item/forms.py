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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].required = True  # Initially set as not required
        self.fields['shoeSize'].required = True  # Initially set as not required

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        
        # Check if category is one of those that don't require size and shoeSize
        if category and category.name in ['Accessories']:  # Replace 'Category1', 'Category2' with your actual category names
            cleaned_data['size'] = None  # Clear size field
            cleaned_data['shoeSize'] = None  # Clear shoeSize field

            self.fields['size'].required = False  # set as not required
            self.fields['shoeSize'].required = False  # set as not required

        elif category and category.name in ['Footwear']:  # Replace 'Category1', 'Category2' with your actual category names
            cleaned_data['size'] = None  # Clear size field

            self.fields['size'].required = False  # set as not required
            self.fields['shoeSize'].required = True  # set as required
        
        elif category and category.name in ['Bottoms', 'Tops', 'Outerwear']:  # Replace 'Category1', 'Category2' with your actual category names
            cleaned_data['shoeSize'] = None  # Clear shoeSize field
            self.fields['size'].required = True  # set as required
            self.fields['shoeSize'].required = False  # set as not required

        return cleaned_data


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].required = False  # Initially set as not required
        self.fields['shoeSize'].required = False  # Initially set as not required

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        
       # Check if category is one of those that don't require size and shoeSize
        if category and category.name in ['Accessories']:  # Replace 'Category1', 'Category2' with your actual category names
            cleaned_data['size'] = None  # Clear size field
            cleaned_data['shoeSize'] = None  # Clear shoeSize field

            self.fields['size'].required = False  # set as not required
            self.fields['shoeSize'].required = False  # set as not required

        elif category and category.name in ['Footwear']:  # Replace 'Category1', 'Category2' with your actual category names
            cleaned_data['size'] = None  # Clear size field

            self.fields['size'].required = False  # set as not required
            self.fields['shoeSize'].required = True  # set as required
        
        elif category and category.name in ['Bottoms', 'Tops', 'Outerwear']:  # Replace 'Category1', 'Category2' with your actual category names
            cleaned_data['shoeSize'] = None  # Clear shoeSize field
            self.fields['size'].required = True  # set as required
            self.fields['shoeSize'].required = False  # set as not required

        return cleaned_data