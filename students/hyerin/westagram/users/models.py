from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)

    email = models.CharField(max_length=50)

    password = models.CharField(max_length=50)

    p_number = models.CharField(max_length=50)


class Meta:
    db_table = 'users'