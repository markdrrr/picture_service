from django.db import models
from django.urls import reverse


class Image(models.Model):
    img = models.ImageField(upload_to='', verbose_name='Картинка', blank=True)

    def __str__(self):
        return f'{self.img}'

    def get_absolute_url(self):
        return reverse('view_image', kwargs={"pk": self.pk})
