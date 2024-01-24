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



# Models for uploading
class clothingCategories(models.Model):
	category = models.CharField(max_length=50)

	def __str__(self):
		return self.category


class clothingStyles(models.Model):
	style = models.CharField(max_length=50)
	

	def __str__(self):
		return self.style

class colors(models.Model):
	color = models.CharField(max_length=15)

	def __str__(self):
		return self.color


class userClothes(models.Model):
	name = models.CharField(max_length=100, default='')
	category = models.ForeignKey(clothingCategories, on_delete=models.CASCADE)
	style = models.ForeignKey(clothingStyles, on_delete=models.CASCADE)
	color = models.ForeignKey(colors, on_delete=models.CASCADE)
	bloguser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return 'http://127.0.0.1:8000/upload/'
