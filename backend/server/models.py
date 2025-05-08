from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)                      # Required
    description = models.TextField(blank=True, null=True)       # Not Required
    
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

    def save(self, *args, **kwargs):
        # @Override channel name to lowercase when saving in DB
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


