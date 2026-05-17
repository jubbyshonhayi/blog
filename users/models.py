from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
        except FileNotFoundError:
            if self.image.name != 'default.jpg':
                self.image = 'default.jpg'
                super().save(update_fields=['image'])
            return
        except (UnidentifiedImageError, ValueError):
            return

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



