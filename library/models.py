from django.db import models


# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    email = models.EmailField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Books(models.Model):
    ISBN = models.CharField(max_length=50)
    publishedYear = models.DateField()
    author = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    img = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.ISBN


class Borrow(models.Model):
    ISBN = models.CharField(max_length=50)
    img = models.ImageField(null=True, blank=True)
    time = models.IntegerField()
    user = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.ISBN
