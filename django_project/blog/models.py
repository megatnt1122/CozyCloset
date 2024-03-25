from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    title = models.CharField(blank=True, max_length=100)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='', null=True, blank=True, upload_to='post_photos')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.name = self.title.title()
        super(Post, self).save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except:
            pass
    
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
		output_size = (600, 600)
		img.thumbnail(output_size)
		img.save(self.image.path)

	def get_absolute_url(self):
		return '/upload/'

class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Top')
    bottoms = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Bottoms')
    footwear = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Footwear')
    accessory = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Accessory', blank=True, null=True)
    outerwear = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Outerwear', blank=True, null=True)

    def __str__(self):
        return f"Outfit for {self.user.username}"


# Models for closets
class Closet(models.Model):
	name = models.CharField(max_length=25, default='')
	closetUser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	is_public = models.BooleanField(default=True, verbose_name="Public")

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		super(Closet, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('my-closets')

class closetClothes(models.Model):
	closet = models.ForeignKey(Closet, on_delete=models.CASCADE, default='')
	clothing_item = models.ForeignKey(userClothes, on_delete=models.CASCADE, default='')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    
class postClothes(models.Model):
	clothing_item = models.ForeignKey(userClothes, on_delete=models.CASCADE, default='')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
