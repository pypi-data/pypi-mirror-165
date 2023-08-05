from random import sample
from string import ascii_uppercase

from django.db import models
from django.urls import reverse

from captcha.image import ImageCaptcha


class Captcha(models.Model):
    LEN = 5
    secret = models.CharField(max_length=LEN)
    image = models.ImageField(blank=True, upload_to="syngo/")

    def get_absolute_url(self):
        return reverse("syngo:check", kwargs={"pk": self.pk})

    def create_image(self):
        name = f"{self.id}.png"
        data = ImageCaptcha().generate(self.secret)
        self.image.save(name, data)

    @staticmethod
    def generate():
        c = Captcha.objects.create(secret="".join(sample(ascii_uppercase, Captcha.LEN)))
        c.create_image()
        return c
