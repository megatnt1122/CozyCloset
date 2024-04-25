from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ShoeSize(models.Model):
     name = models.CharField(max_length=255)

     def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE,default=0)
    name = models.CharField(max_length=255)
    size = models.ForeignKey(Size, related_name='items', on_delete=models.CASCADE,default=1)
    shoeSize = models.ForeignKey(ShoeSize, related_name='items', on_delete=models.CASCADE,default=47)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    