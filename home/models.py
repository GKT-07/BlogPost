from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.db.models.deletion import CASCADE, PROTECT
from froala_editor.fields import FroalaField
from .helpers import *
import uuid


class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000 , null=True , blank=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='blog', blank=True, null=True)
    image = models.ImageField(upload_to='img')
    voted = models.ManyToManyField(User, related_name='votes', default=[0], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    
    
    def save(self , *args, **kwargs): 
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)




    