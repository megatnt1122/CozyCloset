from django.db import models

# Create your models here.
class clothingCategories(models.Model):
	categoryID = models.IntegerField()
	clothingType = models.CharField(max_length=50)

	def __str__(self):
		return self.clothingType


class clothingStyles(models.Model):
	styleID = models.IntegerField()
	styleType = models.CharField(max_length=50)

	def __str__(self):
		return self.styleType


class userClothes(models.Model):
	categoryID = models.ForeignKey(clothingCategories, on_delete=models.CASCADE)
	styleID = models.ForeignKey(clothingStyles, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, default=1)

	def __str__(self):
		return self.name

	


#class Item(models.Model):
#	text = models.CharField(max_length=300)
#	complete = models.BooleanField()
#
#	def __str__(self):
#		return self.text