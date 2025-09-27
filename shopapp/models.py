from django.db import models

class Users(models.Model):
    username = models.EmailField(unique=True)   # email as login username
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('customer', 'Customer')])

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.CharField(max_length=200)  # just store image filename from static folder

    def __str__(self):
        return self.name
