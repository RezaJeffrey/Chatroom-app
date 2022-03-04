from django.db import models
from account.models import User
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import truncatechars


class Room(models.Model):
    room_name = models.CharField(max_length=60)
    members = models.ManyToManyField(User, through='Membership')
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
        self.password = make_password(value)
        return self.password


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = [['room', 'user']]

    def __str__(self):
        if self.room.is_private:
            return f'{self.user}    ---joined-->    {self.room}-(private)'
        return f'{self.user}    ---joined-->    {self.room}'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    posted = models.TimeField(auto_now_add=True)

    @property
    def short_body(self):
        return truncatechars(self.body, 35)

    def __str__(self):
        return self.body


