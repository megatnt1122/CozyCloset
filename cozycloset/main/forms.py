from django import forms

categoryChoices = ( 
    ("1", "Shirt"), 
    ("2", "Pants"), 
    ("3", "Dress"), 
    ("4", "Shoes"), 
) 

styleChoices = (
	("1", "Athletic"),
	("2", "Casual"),
	("3", "Formal"),
	("4", "Lounge")
)

class Upload(forms.Form):
	name = forms.CharField(max_length=100)
	category = forms.ChoiceField(choices=categoryChoices)
	style = forms.ChoiceField(choices=styleChoices)
	

