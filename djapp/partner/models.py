from django.db import models


# Create your models here.
class Partner(models.Model):
    def __str__(self):
        return self.name

    STATUS_LIST = (
        (0, 'Banned'),
        (1, 'Active'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=30)
    status = models.IntegerField(choices=STATUS_LIST)

