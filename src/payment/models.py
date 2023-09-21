from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=(('usd', 'USD'), ('eur', 'EUR')), default='usd')

    def __str__(self):
        return f"{self.name}: {self.price} {self.currency}"


class Order(models.Model):
    order_number = models.CharField(max_length=10)
    items = models.ManyToManyField(Item, related_name='orders')

    def __str__(self):
        return self.order_number

    def total_price(self):
        return sum(item.price for item in self.items.all())

    def get_item_names(self):
        return [item.name for item in self.items.all()]



