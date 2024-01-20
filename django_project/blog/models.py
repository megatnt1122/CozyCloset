from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



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
