from django.db import models
from account.models import User
from django.urls import reverse


class Room(models.Model):
    # TODO backward relations
    room_name = models.CharField(max_length=60)
    users = models.ManyToManyField(User)
    created_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=60)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=50, default='', blank=not is_private, null=not is_private)

    def __str__(self):
        return self.room_name

    def get_absolute_url(self):
        return reverse('room:room_inside', args=[self.id, self.slug])

    def set_is_private(self, value):
        self.is_private = value
        return self.is_private

    def set_password(self, value):
        self.password = value
        return self.is_private


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    posted = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.body


