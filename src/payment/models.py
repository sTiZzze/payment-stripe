from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.name) + ": $" + str(self.price)
