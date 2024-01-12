from django.contrib import admin
from .models import clothingCategories, clothingStyles, userClothes
# Register your models here.
admin.site.register(userClothes)
admin.site.register(clothingStyles)
admin.site.register(clothingCategories)