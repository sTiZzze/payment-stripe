from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.name) + ": $" + str(self.price)


class Order(models.Model):
    order_number = models.CharField(max_length=10)
    items = models.ManyToManyField(Item, related_name='orders')

    def __str__(self):
        return self.order_number

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def get_item_names(self):
        return [item.name for item in self.items.all()]
