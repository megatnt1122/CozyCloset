from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import clothingStyles, clothingCategories, userClothes
from .forms import Upload

# Create your views here.

def home(response):
	return render(response, "main/home.html", {})

def upload(response):
	if response.method == "POST":
		form = Upload(response.POST)

		categories = {1: 'Shirt', 2: 'Pants', 3: 'Dress', 4: 'Shoes'}
		styles = {1: 'Athletic', 2: 'Casual', 3: 'Formal', 4: 'Lounge'}


		if form.is_valid():
			name = form.cleaned_data["name"]
			c = clothingCategories.objects.get(categoryID=(form.cleaned_data["category"]))
			s = clothingStyles.objects.get(styleID=(form.cleaned_data["style"]))
			newUpload = userClothes(categoryID=c, styleID=s, name=name)
			newUpload.save()
			return HttpResponseRedirect("/home")

	else:
		form = Upload()
	return render(response, "main/upload.html", {"form":form})
