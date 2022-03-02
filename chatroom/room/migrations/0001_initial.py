# Generated by Django 4.0.2 on 2022-02-28 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=60)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=60)),
                ('is_private', models.BooleanField(default=False)),
                ('password', models.CharField(default='', max_length=50)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(blank=True, max_length=200, null=True)),
                ('posted', models.TimeField(auto_now_add=True)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='room.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]