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
    likes = models.ManyToManyField(User, related_name='blog_posts')
    
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.name = self.title.title()
        super(Post, self).save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
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
    name = models.CharField(max_length=25, default='', verbose_name='Name')
    category = models.ForeignKey(clothingCategories, on_delete=models.CASCADE, verbose_name='Category')
    style = models.ForeignKey(clothingStyles, on_delete=models.CASCADE, verbose_name='Style')
    color = models.ForeignKey(colors, on_delete=models.CASCADE, verbose_name='Color')
    image = models.ImageField(default='', upload_to='clothing_photos')
    bloguser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(userClothes, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        output_size = (1200, 1200)
        img.thumbnail(output_size)
        img.save(self.image.path)

    def get_absolute_url(self):
        return '/upload/'

class Outfit(models.Model):
    name = models.CharField(max_length=25, default='', verbose_name='Name')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Top')
    bottoms = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Bottoms')
    footwear = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Footwear')
    accessory = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Accessory', blank=True, null=True)
    outerwear = models.ForeignKey(userClothes, on_delete=models.CASCADE, related_name='Outerwear', blank=True, null=True)

    def __str__(self):
        return self.name

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

class closetOutfits(models.Model):
    closet = models.ForeignKey(Closet, on_delete=models.CASCADE, default='')
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)

class postClothes(models.Model):
    clothing_item = models.ForeignKey(userClothes, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)

class Convo(models.Model):
    user = models.ForeignKey(User, related_name='convoUser', on_delete=models.CASCADE, default=1)
    members = models.ManyToManyField(User, related_name='convos')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)


class ConvoMessage(models.Model):
    conversing = models.ForeignKey(Convo, related_name='convoMessage', on_delete=models.CASCADE, default=1)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='created_message', on_delete=models.CASCADE, default=1)

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    #commentuser = models.ForeignKey(User, related_name='created_comment', on_delete=models.CASCADE, default=1)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
