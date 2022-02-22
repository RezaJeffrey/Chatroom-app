from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    posted = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class Room(models.Model):
    room_name = models.CharField(max_length=60)
    users = models.ManyToManyField(User)
    created_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=60)

    def __str__(self) :
        return self.room_name

    def get_absolute_url(self):
        return reverse('room:room_inside', args=[self.id, self.slug])

