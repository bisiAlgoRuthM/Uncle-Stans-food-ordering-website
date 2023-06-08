from django.db import models

# Create your models here.
from django.db import models

class OrderModel(models.Model):
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    def __str__(self):
        return f"Order #{self.id} - {self.created_at.strftime('%b %d %I %M %p')}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    items = models.ManyToManyField(MenuItem)

    def calculate_total(self):
        return sum(item.price for item in self.items.all())