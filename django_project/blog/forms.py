from django import forms

class Upload(forms.Form):
	colorChoices = ['black', 'white', 'red', 'green', 'yellow', 'blue', 'brown', 'orange', 'pink', 'purple', 'grey']
	categoryChoices = ['Shirt', 'Jacket', 'Pants', 'Dress', 'Shoes']
	styleChoices = ["Athletic", "Casual", "Formal", "Lounge"]
	name = forms.CharField(max_length=100)
	category = forms.ChoiceField(choices=categoryChoices)
	style = forms.ChoiceField(choices=styleChoices)
	color = forms.ChoiceField(choices=colorChoices)
	

