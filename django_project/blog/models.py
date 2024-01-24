from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


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
	image = models.ImageField(default='default.jpg', upload_to='clothing_photos')
	bloguser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		super(userClothes, self).save(*args, **kwargs)
		img = Image.open(self.image.path)
		img.save(self.image.path)

		#if img.height > 1000 or img.width > 1000:
			#output_size = (1000, 1000)
			#img.thumbnail(output_size)
			#img.save(self.image.path)

	def get_absolute_url(self):
		return 'http://127.0.0.1:8000/upload/'
