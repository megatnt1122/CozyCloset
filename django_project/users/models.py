from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Closet(models.Model):
    closet = models.OneToOneField(Closet, on_delete=models.CASCADE)
    closet_image = models.ImageField(default='C.png', upload_to='closet_pics')

    def __str__(self):
        return f'{self.closet.username} Closet'

    def save(self, *args, **kwargs):
        super(Closet, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (450, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)
