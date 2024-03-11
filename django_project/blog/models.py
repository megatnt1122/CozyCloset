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
    
    image = models.ImageField(default='default.jpg', upload_to='clothing_photos')
    #Need to change to default.jpg to see differents
    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        #if (img = 'default.jpg'):
            #img = None
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        print(img)

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
	name = models.CharField(max_length=25, default='', verbose_name='*Name')
	category = models.ForeignKey(clothingCategories, on_delete=models.CASCADE, verbose_name='*Category')
	style = models.ForeignKey(clothingStyles, on_delete=models.CASCADE, verbose_name='*Style')
	color = models.ForeignKey(colors, on_delete=models.CASCADE, verbose_name='*Color')
	image = models.ImageField(default='', upload_to='clothing_photos')
	bloguser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		super(userClothes, self).save(*args, **kwargs)
		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

	def get_absolute_url(self):
		return '/upload/'

# Models for closets
class Closet(models.Model):
	name = models.CharField(max_length=25, default='')
	closetUser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		super(Closet, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('open-closet', kwargs={'closetid': self.id})

class closetClothes(models.Model):
	closet = models.ForeignKey(Closet, on_delete=models.CASCADE, default='')
	clothing_item = models.ForeignKey(userClothes, on_delete=models.CASCADE, default='')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    
#class postClothes(models.Model):
	#clothing_item = models.ForeignKey(userClothes, on_delete=models.CASCADE, default='')
	#user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
