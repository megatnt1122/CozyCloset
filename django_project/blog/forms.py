<<<<<<< HEAD
from django import forms

class Upload(forms.Form):
	colorChoices = ['black', 'white', 'red', 'green', 'yellow', 'blue', 'brown', 'orange', 'pink', 'purple', 'grey']
	categoryChoices = ['Shirt', 'Jacket', 'Pants', 'Dress', 'Shoes']
	styleChoices = ["Athletic", "Casual", "Formal", "Lounge"]
	name = forms.CharField(max_length=100)
	category = forms.ChoiceField(choices=categoryChoices)
	style = forms.ChoiceField(choices=styleChoices)
	color = forms.ChoiceField(choices=colorChoices)
	

<<<<<<< Updated upstream
=======
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
	

>>>>>>> main
=======
>>>>>>> Stashed changes
