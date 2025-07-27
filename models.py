# Create your models here.
from django.db import models

class UserData(models.Model):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    mobno = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=128)  # Use hashed password later
    usertype = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.usertype})"

    class Meta:
        db_table = "userdata"
