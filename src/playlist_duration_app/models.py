from django.db import models

# Create your models here.
class playlistLinkForm(models.Model):
	link = models.CharField(max_length=150)
