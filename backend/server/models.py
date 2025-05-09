from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension


def server_icon_upload_path(instance, filename):
    return f'server/{instance.id}/server_icon/{filename}'

def server_banner_upload_path(instance, filename):
    return f'server/{instance.id}/server_banner/{filename}'

def category_icon_upload_path(instance, filename):
    return f'category/{instance.id}/category_icon/{filename}'



class Category(models.Model):
    name = models.CharField(max_length=50)                      # Required
    description = models.TextField(blank=True, null=True)       # Not Required
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.id:     # Category already exists
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)        # Replace icon
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender='server.Category')
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)
    
    
    def __str__(self):
        return self.name



class Server(models.Model):
    name = models.CharField(max_length=100)                      # Required
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,         # if user is deleted, server goes too
                              related_name='server_owner')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='server_category')    # 1 category has many servers
    description = models.CharField(max_length=250, null=True)       # Not Required
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)       # Many members belong to many servers, many servers have many memebers
    # icon

    def __str__(self):
        return self.name



class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channel_owner')     # 1 owner has many channels
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channel_server')     # 1 server has many channels
    banner = models.ImageField(
        upload_to=server_banner_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension]
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension, validate_icon_image_size]
    )

    def save(self, *args, **kwargs):
        if self.id:     # Channel already exists
            existing = get_object_or_404(Category, id=self.id)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)        # Replace icon
            if existing.icon != self.icon:
                existing.icon.delete(save=False)        # Replace icon
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender='server.Server')
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon' or field.name == 'banner':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name


